import base64
from django.shortcuts import render
from .functions import generate_story,generate_image_stability,generate_voice
from . import models
import os
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
import json
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def home(request):    
    context = {"loggedin": "false"}
    
    if request.user.is_authenticated:
        context.update({
            "loggedin": "true",
            "name": request.user.first_name,
            "username": request.user.username
        })
    print(context)    
    return render(request, 'index.html', context)

def generate(request):
    if request.method == 'POST':
        perspective = request.POST.get('pres', 'first') 
        prompt = request.POST.get('prompt', '')
        

        print(f"Perspective: {perspective}")
        print(f"Prompt: {prompt}")
        title,prompt, story_content = generate_story(prompt,perspective)
        story = models.Story.objects.create(
            user=request.user,  
            title=title,
            content=story_content,
        )
        image = generate_image_stability(prompt)
        # image.save(filename)
        with open(f"static/story_images/{story.story_id}.png", "wb") as f:
            f.write(base64.b64decode(image)) 

        story_content = story_content.replace(r"\n", "<br>")

        generate_voice(story_content,f"static/story_audio/{story.story_id}.wav")
        # generate_voice, story_content, file_name
        return render(request, 'story.html', {
            'title' : title,
            'story_content': story_content,
            'story_id':story.story_id
        })

    
    return render(request, 'generate.html')

def landing(request):
    if request.method == 'POST':
        search_term = request.POST.get('query', '')  
        stories = models.Story.objects.select_related('user').filter(title__icontains=search_term).order_by('-created_at')
    else:
        stories = models.Story.objects.select_related('user').all().order_by('-created_at')
    
    context = {
        'stories': stories,
    }
    
    return render(request, 'landing.html', context)

def story_detail(request, story_id):
    try:
        story = models.Story.objects.get(story_id=story_id)

        story_content = story.content.replace(r"\n", "<br>")
        
        return render(request, 'story.html', {
            'title': story.title,
            'story_content': story_content,
            'story_id': story.story_id
        })
    except models.Story.DoesNotExist:
        return render(request, '404.html') 

def ask_gpt(request):
    print("bro")
    data = json.loads(request.body)
    title = data.get('title')
    content = data.get('content')
    question = data.get('question')

    # Retrieve the story from the database
    try:
        story = models.Story.objects.get(title=title)
        story_content = story.content
    except models.Story.DoesNotExist:
        return JsonResponse({"error": "Story not found"}, status=404)

    system_msg = (
        "You are an assistant that answers the questions to the children's "
        "story given below. You should answer the questions descriptively in a "
        "way that a child can understand them. If the question asked is unrelated "
        "to the story, do not answer the question and instead reply by asking the "
        "user to ask questions related to the story."
        "\n\n"
        f"Story: {story_content}"
    )

    # Prepare the messages for the OpenAI API
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": question}
    ]

    # Call OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # Get the response content
    answer = completion.choices[0].message.content

    # Return the response as JSON
    return JsonResponse({"answer": answer})

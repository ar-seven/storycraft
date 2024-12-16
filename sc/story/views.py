import base64
from django.shortcuts import render
from .functions import generate_story,generate_image_stability,generate_voice
from . import models
# Create your views here.
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

# Create your views here.
def generate(request):
    if request.method == 'POST':
        perspective = request.POST.get('pres', 'first')  # Default to first person if not specified
        prompt = request.POST.get('prompt', '')
        

        print(f"Perspective: {perspective}")
        print(f"Prompt: {prompt}")
        title,prompt, story_content = generate_story(prompt,perspective)
                # Create and save the story to database
        story = models.Story.objects.create(
            user=request.user,  # Current logged-in user
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
        # You might want to redirect to a story page or return the generated story
        return render(request, 'story.html', {
            'title' : title,
            'story_content': story_content,
            'story_id':story.story_id
        })

    
    return render(request, 'generate.html')

def landing(request):
    if request.method == 'POST':
        search_term = request.POST.get('query', '')  # Get the search term from the POST request
        stories = models.Story.objects.select_related('user').filter(title__icontains=search_term).order_by('-created_at')
    else:
        stories = models.Story.objects.select_related('user').all().order_by('-created_at')
    
    context = {
        'stories': stories,
    }
    
    return render(request, 'landing.html', context)

def story_detail(request, story_id):
    try:
        # Get the story from database using story_id
        story = models.Story.objects.get(story_id=story_id)
        
        # Format the story content for HTML display
        story_content = story.content.replace(r"\n", "<br>")
        
        return render(request, 'story.html', {
            'title': story.title,
            'story_content': story_content,
            'story_id': story.story_id
        })
    except models.Story.DoesNotExist:
        # Handle case when story is not found
        return render(request, '404.html')  # Create a 404 template or handle differently

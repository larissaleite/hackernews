import datetime

from django.template import loader, Context, RequestContext

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from stories.models import Story
from stories.forms import StoryForm

from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required

def score(story, gravity=1.8, timebase=120):
  points = story.points**0.8
  now = datetime.datetime.utcnow().replace(tzinfo=utc)
  age = int((now - story.created_at).total_seconds())/60

  return points/(age+timebase)**gravity

def top_stories(top=180, consider=1000):
  latest_stories = Story.objects.all().order_by('-created_at')[:consider]
  ranked_stories = sorted([(score(story), story) for story in latest_stories], reverse=True)
  return [story for _, story in ranked_stories][:top]

# Create your views here.
def index(request):
  stories = top_stories(top=30)
  '''template = loader.get_template('stories/index.html')
  context = Context({'stories':stories})
  response = template.render(context)
  return HttpResponse(response)'''
  context = RequestContext(request, {
    'stories' : stories,
    'user' : request.user #doesn't matter if the user is logged in or not
  })
  return render(request, 'stories/index.html', context)

@login_required
def story(request):
  if request.method == 'POST':
    form = StoryForm(request.POST)
    if form.is_valid():
      story = form.save(commit=False) #creates an instance of the form but does not save
      story.moderator = request.user
      story.save()
      return HttpResponseRedirect('/')
  else:
    form = StoryForm()

  return render(request, 'stories/story.html', { 'form' : form })

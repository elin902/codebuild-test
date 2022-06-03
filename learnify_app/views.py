from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404


def index(request):
    """Home page of Learnify."""
    if request.user.is_authenticated:
        return render(request, 'learnify_app/authenticated_index.html')
    else:
        return render(request, 'learnify_app/index.html')


@login_required
def topics(request):
    """View all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learnify_app/topics.html', context)


@login_required
def topic(request, topic_id):
    """Display current topic and all related entries."""
    topic = Topic.objects.get(id=topic_id)
    # Making sure if topic is owned by current user
    check_topic_owner(topic.owner, request)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learnify_app/topic.html', context)


@login_required
def new_topic(request):
    """Add new topic"""

    if request.method != 'POST':
        # No data passed, create empty form.
        form = TopicForm()
    else:
        # Data passed with POST, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learnify_app:topics')

    # Display empty form
    context = {'form': form}
    return render(request, 'learnify_app/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add new entry"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data passed, create empty form.
        form = EntryForm()
    else:
        # Data passed with POST, process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('learnify_app:topic', topic_id=topic_id)
    # Display empty form
    context = {'topic': topic, 'form': form}
    return render(request, 'learnify_app/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Check if current user has rights to edit
    check_topic_owner(topic.owner, request)

    # Passing data
    if request.method != 'POST':
        # Initial request, filling form with updated value.
        form = EntryForm(instance=entry)
    else:
        # Data passed with POST, process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learnify_app:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learnify_app/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    """Delete entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic.owner, request)

    if request.method == 'POST':
        entry.delete()
        return redirect('learnify_app:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic}
    return render(request, 'learnify_app/edit_entry.html', context)


def check_topic_owner(owner, request):
    """Checks if topic owner is the current user"""
    if owner != request.user:
        raise Http404

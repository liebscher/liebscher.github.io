Title: Modern Day Psychography (Part 1)
Date: 2022-11-29
Tags: python
Category: meta
Slug: modern-day-psychography-1
Authors: Alex Liebscher
Summary: Speech-to-Text and Séance with my Journal
Status: draft
<!-- Cover: images/window-overlooking-green-pasture.png -->

This is the first part in a series.

Creating a py 3.10 env

One of my strongest habits is journaling. I try to journal everyday and, I've accumulated a rich picture of my life that I'm proud of. Being the linguaphile I am, I wondered: what patterns and insights might emerge in this narrative of my life?

This post describes how I'm approaching the problem from the very beginning. The end product is a Jupyter notebook where I can record myself reading out loud my journal, which then gets transcribed and organized onto my computer. For perspective, I was able to get the majority of this notebook written in about 15 minutes.

## Dictating my Journal

The first part is to load up a few packages and a model we'll need. I'm making use of Jupyter Notebooks right now. OpenAI's latest [whisper](https://github.com/openai/whisper) model has really impressed me; both because it's open-source and because it works well.

    :::python
    import json

    import pendulum

    from ipywebrtc import AudioRecorder, CameraStream
    from IPython.display import Audio

    import whisper

    model = whisper.load_model("base")

Next we need an interface to record the audio. We'll use a Jupyter widget for that, which I learned about via [a Medium post](https://medium.com/@harrycblum/record-audio-in-a-jupyter-notebook-da08a88278bb).

    :::python
    camera = CameraStream(constraints={'audio': True,'video':False})
    recorder = AudioRecorder(stream=camera)
    recorder

After we have the audio sorted out, we save that memory-based audio to a file and have whisper load that file to transcribe it. ffmpeg here is crucial for converting the audio, although I'd really like to find a way to just keep the audio in memory.

    :::python
    with open('recording.webm', 'wb') as f:
        f.write(recorder.audio.value)
    
    !ffmpeg -i recording.webm -ac 1 -f wav file.wav -y -hide_banner -loglevel panic

    result = model.transcribe("file.wav")

    !rm recording.webm

Lastly, we can view the out from that model.

    :::python
    text_out = result['text']
    text_out[:50] + '...'

<pre class="code-output" style="overflow:">
" September 26th, 2021. One behavior I'd like to try would be the annual quarterly and monthly reviews. I could start by breaking down the last of each period using my previous journal, perhaps tonight I will. Well, I started to read backwards one month, then two, and then maybe three. It's hard to summarize more than just factual events. I should attempt to capture more emotion and internal dialogue, especially with regards to work. Three things I'm grateful for, a healthy body, Kaelin's unwavering support, and being illiterate.
</pre>

It's pretty good, although it messed up a few things. Notably, Kaelin should be Kaylin (although even she would agree it's hard to spell this based on audio), illiterate should crucially be literate, and it seems to have skipped the commas I had in the first sentence.

## Organization

Naturally, we want to save this text to our computer so that we can comes back to it. Here we'll take a first step towrad that.

The path of least resistance for me is to have this recorded text in a JSON file.

    :::python
    try:
        with open('notebook.json', 'r') as fh:
            notebook = json.load(fh)
    except FileNotFoundError:
        notebook = {}

    print(f"{len(notebook)} existing entries")

With a `notebook` object ready to use, we want to organize our new data in a dictionary with dates as keys and entries as values.

I was interested in trying out the `pendulum` library for parsing dates. The API looks great, unfortunately the project is only lightly maintained so issues may arise and not be fixed. However, in my case here it's not an a problem.

I wanted to make sure I didn't accidentally overwrite an entry, so we check if something already exists for that date. If it does we prompt the user about it.

    :::python
    date = pendulum.from_format(text_out.split('.')[0].strip(), 'MMMM Do, YYYY', tz='America/Los_Angeles')
    date_str = date.to_date_string()

    write = True

    if date_str in notebook:
        write = (input('Date exists, overwrite? [y|n]') == 'y')

    if write:
        notebook[date_str] = '.'.join(text_out.split('.')[1:]).strip()
        with open('notebook.json', 'w') as fh:
            json.dump(notebook, fh)
        
        print('Entry saved!')

I'm not saving the audio file, which I think is okay but I might regret that.

As a quick example of what value this now provides, something I've always been interested in is about how many words my journal entries are. I'm too lazy to count them, so let's just have Python do it instead.

    :::python
    {k: len(v.split()) for k, v in notebook.items()}

That concludes this first part.
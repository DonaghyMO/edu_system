from resource_manage.models import Audio

if __name__ == '__main__':
    audios = Audio.objects.filter(category_id=21)
    for audio in audios:
        print(audio.title)
        print(audio.audio_file.split("audio/")[0])

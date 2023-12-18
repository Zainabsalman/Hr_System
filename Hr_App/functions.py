def handle_uploaded_file(file):
    with open('static/img/announcement_images/'+file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def handle_uploaded_file2(file):
    with open('static/cvs/'+file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
import csv
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import face_recognition
from PIL import Image, ImageDraw
import numpy as np
import cv2
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from cases.models import CasesModel
from .forms import CitizenForm
from .models import CitizenProfile, SpottedCitizen
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@login_required
# @method_decorator(login_required, name='dispatch')
def add_staff(request):
    return render(request, 'accounts/register.html')


@method_decorator(login_required, name='dispatch')
class AddCitizen(CreateView):
    template_name = 'detection/add_citizen.html'
    form_class = CitizenForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        # import pdb;pdb.set_trace()
        if form.is_valid():
            form.save()
            messages.success(request, 'Citizen saved successfully')
            return redirect('detection:view-citizen')

        messages.error(request, 'Please check your credentials again')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ListCitizenView(ListView):
    template_name = 'detection/view_citizen.html'
    model = CitizenProfile
    context_object_name = 'citizens'


@login_required
def delete_citizen(request, pk):
    try:
        citizen = CitizenProfile.objects.get(pk=pk)
    except CitizenProfile.DoesNotExist:
        messages.error(request, "Citizen not found")
        return redirect('detection:view-citizen')
    citizen.delete()
    messages.success(request, "Citizen deleted successfully")
    return redirect('detection:view-citizen')


@method_decorator(login_required, name='dispatch')
class UpdateCitizenView(UpdateView):
    model = CitizenProfile
    form_class = CitizenForm
    template_name = 'detection/update_citizen.html'
    success_url = reverse_lazy('detection:view-citizen')

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES)
    #     # import pdb;pdb.set_trace()
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Citizen Updated successfully')
    #         return redirect('detection:view-citizen')
    #
    #     messages.error(request, 'Please check your credentials again')
    #     return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class SpottedCitizenView(ListView):
    model = SpottedCitizen
    template_name = 'detection/spotted_citizen.html'
    context_object_name = 'citizens'
    paginate_by = 5


@login_required
def citizen_location(request, pk):
    wanted_citizen = SpottedCitizen.objects.filter(pk=pk)
    context = {
        "citizen_location": wanted_citizen
    }
    return render(request, 'detection/location.html', context)


@login_required
def found_citizen(request, pk):
    free = SpottedCitizen.objects.filter(pk=pk)
    freecitizen = SpottedCitizen.objects.filter(id=free.get().id).update(status='Found')
    if freecitizen:
        citizen = SpottedCitizen.objects.filter(pk=pk)
        free = CasesModel.objects.filter(id=citizen.get().id).update(status='Found')
        if free:
            messages.success(request, messages.INFO, "Citizen updated to found, congratulations")
        else:
            messages.error(request, "Failed to update citizen status")
    return redirect('detection:spotted-citizen')


@login_required
def csv_database_write(request, pk):
    # Get all data from UserDetail Database Table
    try:
        citizen = CitizenProfile.objects.get(pk=pk)
    except CitizenProfile.DoesNotExist:
        messages.error(request, "Citizen not found")
        return redirect('detection:view-citizen')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Details.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'address', 'phone_number',
                     'nationality', 'citizenship_number',
                     'bio', 'citizenship_image', 'status', 'birth_date'])

    writer.writerow([citizen.first_name, citizen.last_name, citizen.address, citizen.phone_number,
                     citizen.nationality, citizen.citizenship_number, citizen.bio,
                     citizen.citizen_image, citizen.status, citizen.birth_date])

    return response


@login_required
# @method_decorator(login_required, name='dispatch')
def detect_image(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        # fs = FileSystemStorage(base_url='media/uploads')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # img_upload = FileSystemStorage(location='media/uploads')
        # img_save = img_upload.save(myfile.name, myfile)
        # img_file_url = img_upload.url(img_save)

    images = []
    encodings = []
    names = []
    files = []
    case_id = []
    # citizenship_number = []

    cases = CasesModel.objects.all()
    for crime in cases:
        images.append(crime.first_name + '_image')
        encodings.append(crime.first_name + '_face_encoding')
        files.append(crime.image)
        names.append(crime.first_name + ' ' + crime.last_name)
        case_id.append(crime.id)

    # citizen = CitizenProfile.objects.all()
    # for crime in citizen:
    #     images.append(crime.first_name + '_image')
    #     encodings.append(crime.first_name + '_face_encoding')
    #     files.append(crime.citizen_image)
    #     names.append(crime.first_name + ' ' + crime.last_name)
    #     citizenship_number.append(crime.citizenship_number)

    for i in range(0, len(images)):
        try:
            images[i] = face_recognition.load_image_file(files[i])
            encodings[i] = face_recognition.face_encodings(images[i])[0]
        except IndexError:
            messages.INFO(request, 'Not able to locate any faces.')
            print("Not able to locate any faces in at least one of the images. Check the image files. Aborting...")
            return redirect('accounts:dashboard')

    # Create arrays of known face encodings and their names
    known_face_encodings = encodings
    known_face_names = names
    c_id = case_id
    # c_id = citizenship_number

    # import pdb
    # pdb.set_trace()

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(uploaded_file_url[1:])

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            ca_id = c_id[best_match_index]
            person = CasesModel.objects.filter(id=ca_id)
            name = known_face_names[best_match_index] + ', status: ' + person.get().status
            print('found')

            if person.get().status == 'Wanted':
                wanted_citizen = SpottedCitizen.objects.create(
                    first_name=person.get().first_name,
                    last_name=person.get().last_name,
                    address=person.get().address,
                    contact_number=person.get().contact_number,
                    nationality=person.get().nationality,
                    image=person.get().image,
                    description=person.get().description,
                    gender=person.get().gender,
                    status='Wanted',
                    latitude=0,
                    longitude=0
                )
                wanted_citizen.save()
            elif person.get().status == 'Missing':
                missing_citizen = SpottedCitizen.objects.create(
                    first_name=person.get().first_name,
                    last_name=person.get().last_name,
                    address=person.get().address,
                    contact_number=person.get().contact_number,
                    nationality=person.get().nationality,
                    image=person.get().image,
                    description=person.get().description,
                    gender=person.get().gender,
                    status='Missing',
                    latitude=0,
                    longitude=0
                )
                missing_citizen.save()
            else:
                pass

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    if draw:
        # Remove the drawing library from memory as per the Pillow docs
        del draw

        # Display the resulting image
        pil_image.show()
        return redirect('cases:list-case')

        # You can also save a copy of the new image to disk if you want by uncommenting this line
        # pil_image.save("image_with_boxes.jpg")

    else:
        print('try again')


@login_required
def detect_video(request):
    # upload image
    myfile = []

    if request.method == 'POST' and request.FILES['video']:
        myfile = request.FILES['video']
        print("video poseted")
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # Create an output movie file (make sure resolution/frame rate matches input video!)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('output.avi', fourcc, 29.97, (640, 360))

    images = []
    encodings = []
    names = []
    files = []
    case_id = []
    frame_number = 0

    citizen = CasesModel.objects.all()
    for crime in citizen:
        images.append(crime.first_name + '_video')
        encodings.append(crime.first_name + '_face_encoding')
        files.append(crime.image)
        names.append(crime.first_name + crime.last_name)
        case_id.append(crime.id)

    for i in range(0, len(images)):
        images[i] = face_recognition.load_image_file(files[i])
        encodings[i] = face_recognition.face_encodings(images[i])[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = encodings
    known_face_names = names
    c_id = case_id

    unknown_image = cv2.VideoCapture(uploaded_file_url[1:])

    while True:
        # Grab a single frame of video
        ret, frame = unknown_image.read()
        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # If you had more than 2 faces, you could make this logic a lot prettier
            # but I kept it simple for the demo

            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                print("match")
                ca_id = c_id[best_match_index]
                person = CasesModel.objects.filter(id=ca_id)
                name = known_face_names[best_match_index] + ', status: ' + person.get().status

                if person.get().status == 'Wanted':
                    wanted_citizen = SpottedCitizen.objects.create(
                        first_name=person.get().first_name,
                        last_name=person.get().last_name,
                        address=person.get().address,
                        contact_number=person.get().contact_number,
                        nationality=person.get().nationality,
                        image=person.get().image,
                        description=person.get().description,
                        gender=person.get().gender,
                        status='Wanted',
                        latitude=0,
                        longitude=0
                    )
                    wanted_citizen.save()
                elif person.get().status == 'Missing':
                    missing_citizen = SpottedCitizen.objects.create(
                        first_name=person.get().first_name,
                        last_name=person.get().last_name,
                        address=person.get().address,
                        contact_number=person.get().contact_number,
                        nationality=person.get().nationality,
                        image=person.get().image,
                        description=person.get().description,
                        gender=person.get().gender,
                        status='Wanted',
                        latitude=0,
                        longitude=0
                    )
                    missing_citizen.save()
                else:
                    pass


            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('Video', frame)


        # # Write the resulting image to the output video file
        # print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)

    # All done!
    # myfile.release()
    cv2.destroyAllWindows()
    return redirect('accounts:dashboard')


@login_required
def detect_with_webcam(request):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    images = []
    encodings = []
    names = []
    files = []
    case_id = []
    # citizenship_number = []

    cases = CasesModel.objects.all()
    for crime in cases:
        images.append(crime.first_name + '_image')
        encodings.append(crime.first_name + '_face_encoding')
        files.append(crime.image)
        names.append(crime.first_name + ' ' + crime.last_name)
        case_id.append(crime.id)

    # citizen = CitizenProfile.objects.all()
    # for crime in citizen:
    #     images.append(crime.first_name + '_image')
    #     encodings.append(crime.first_name + '_face_encoding')
    #     files.append(crime.citizen_image)
    #     names.append(crime.first_name + crime.last_name)
    #     citizenship_number.append(crime.citizenship_number)

    for i in range(0, len(images)):
        images[i] = face_recognition.load_image_file(files[i])
        encodings[i] = face_recognition.face_encodings(images[i])[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = encodings
    known_face_names = names
    c_id = case_id

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]
        if rgb_frame is None:
            print('No image')

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                ca_id = c_id[best_match_index]
                person = CasesModel.objects.filter(id=ca_id)
                name = known_face_names[best_match_index] + ', status: ' + person.get().status

                if person.get().status == 'Wanted':
                    wanted_citizen = SpottedCitizen.objects.create(
                        first_name=person.get().first_name,
                        last_name=person.get().last_name,
                        address=person.get().address,
                        contact_number=person.get().contact_number,
                        nationality=person.get().nationality,
                        image=person.get().image,
                        description=person.get().description,
                        gender=person.get().gender,
                        status='Wanted',
                        latitude='20202020',
                        longitude='040404040'
                    )
                    wanted_citizen.save()
                elif person.get().status == 'Missing':
                    missing_citizen = SpottedCitizen.objects.create(
                        first_name=person.get().first_name,
                        last_name=person.get().last_name,
                        address=person.get().address,
                        contact_number=person.get().contact_number,
                        nationality=person.get().nationality,
                        image=person.get().image,
                        description=person.get().description,
                        gender=person.get().gender,
                        status='Missing',
                        latitude='20202020',
                        longitude='040404040'
                    )
                    missing_citizen.save()
                else:
                    pass

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return redirect('accounts:dashboard')

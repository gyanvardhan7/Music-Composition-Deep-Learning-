import pickle,glob
import numpy
from music21 import converter,instrument, note, stream, chord
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import *
from keras.layers import Activation
import os





def get_notes():
    """ Get all the notes and chords from the midi files in the ./ClassicalMIDI directory """
    notes = []

    for file in glob.glob("composer/media/composer/userUpload/userUpload.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    # with open('data/userNotes', 'wb') as filepath:
    #     pickle.dump(notes, filepath)

    return notes


def generate():
    """ Generate a piano midi file """
    # load the notes Mnotes used to train the model
    with open('composer/trainedModel/notesB', 'rb') as filepath:
        Mnotes = pickle.load(filepath)


    print('Creating your Music')


    notes = get_notes() #notes input by users

    # Get all pitch names
    pitchnames = sorted(set(item for item in Mnotes))
    # Get all pitch names
    n_vocab = len(set(Mnotes))

    normalized_user_input = prepare_sequences(Mnotes,notes,pitchnames, n_vocab)

    # print(numpy.shape(normalized_input))

    model = create_network_Bi(n_vocab)
    prediction_output = generate_notes(model,normalized_user_input, pitchnames, n_vocab)
    create_midi(prediction_output)



def prepare_sequences(Mnotes, notes, pitchnames, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    # map between notes and integers and back
    note_to_int = dict((Mnote, number) for number, Mnote in enumerate(pitchnames))

    sequence_length = 100
    # network_input = []
    user_input =[]
    # output = []

    for char in notes: user_input.append(note_to_int[char])

    # user_input.append((note_to_int[char] for char in notes)

    if(len(user_input)<sequence_length):
        for i in range(0,sequence_length-len(user_input),1):
            user_input.append(0)
    else:
        user_input = user_input[0:100]


    normalized_user_input = [x / n_vocab for x in user_input]
    

    return (normalized_user_input)



# # Creating the Neural Network and loading it with Weights

# In[10]:

def create_network_Bi(n_vocab):
    """ create the structure of the Bidirectional LSTM neural network """
    model = Sequential()
    model.add(Bidirectional(LSTM(512,return_sequences=True),input_shape=(100, 1),merge_mode='concat'))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(512, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(512)))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    # Load the weights to each node
    
    #RNN weights
    model.load_weights('composer/trainedModel/new_weightsB.hdf5')
    

    return model




def create_network(n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(100, 1),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    # Load the weights to each node
    model.load_weights('composer/trainedModel/new_weights.hdf5')

    return model



# # Generate Notes using The Neural Network

# In[11]:


def generate_notes(model,normalized_user_input, pitchnames, n_vocab):
    """ Generate notes from the neural network based on a sequence of notes """
    # pick a random sequence from the input as a starting point for the prediction
    #start = numpy.random.randint(0, len(network_input)-1)


    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    # pattern = network_input[start]
    pattern = normalized_user_input
    prediction_output = []

    # generate 500 notes
    for note_index in range(500):
        prediction_input = numpy.reshape(pattern, (1, len(pattern), 1))
        # prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        index = numpy.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return prediction_output



# # Creating the MIDI output file of the generated sequence

# In[12]:


def create_midi(prediction_output):
    """ convert the output from the prediction to notes and create a midi file
        from the notes """
    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern is a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 0.5

    midi_stream = stream.Stream(output_notes)

    midi_stream.write('midi', fp='composer/static/composer/output/output.mid')


    # convert midi output into Mp3
    os.system('musescore composer/static/composer/output/output.mid -o composer/static/composer/output/play.mp3')

    # create music sheet in png format and XML
    midi_stream.write('musicxml.png',fp='composer/static/composer/musicSheets/musicxml.xml')


# In[14]:


generate()
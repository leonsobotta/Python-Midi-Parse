# File name: midi_parse.py
# Description: Parse midi files and save contents in .h file
# Author: Leon Sobotta
# Date: 15.06.2021

from os import X_OK
import pretty_midi
import argparse


def getSongNames():
    """Obtain the midi-filenames from the user via command line. 
    Input will be saved and appended into an array
    """

    global namen

    namen = []
    temp = []

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--song1", required = True, default = None, type= str, help= "Name vom ersten Song, welcher verarbeitet werden soll.")
    parser.add_argument("--song2", required = False, default = None, type= str, help= "Name vom zweiten Song, welcher verarbeitet werden soll.")
    parser.add_argument("--song3", required = False, default = None, type= str, help= "Name vom dritten Song, welcher verarbeitet werden soll.")
    parser.add_argument("--song4", required = False, default = None, type= str, help= "Name vom vierten Song, welcher verarbeitet werden soll.")
    parser.add_argument("--song5", required = False, default = None, type= str, help= "Name vom fünften Song, welcher verarbeitet werden soll.")

    args = parser.parse_args()

    opt1_value = args.song1
    opt2_value = args.song2
    opt3_value = args.song3
    opt4_value = args.song4
    opt5_value = args.song5
    
    temp.extend((opt1_value, opt2_value, opt3_value, opt4_value, opt5_value))#saves song names in temp-array

    for name in temp:
        if name != None: #if elemtent in temp-array is not None, it will be appended into the namen array
            namen.append(name)

def openHFile():
    """
    Open/Create the header-file to save the obtained data from the midi-file
    """
    global file2write
    
    file2write=open("Core/Inc/songs.h",'w')

def openMidi():
    """Open midi-file with current index of name-array. It doesn't matter if suffix is included or not.
    """
    global midi_data
    
    if namen[i] != None:
        puffer = namen[i][(len(namen[i])-4):] # saves the last 4 elements of the current string
    
        if puffer == ".mid":    # if the last 4 elements of the current name are .mid, call function without adding the file suffix. Else add .mid suffix
            midi_data = pretty_midi.PrettyMIDI(namen[i])
        else:
            midi_data = pretty_midi.PrettyMIDI(namen[i]+".mid")

def getTempo():
    """Obtain Tempo of current song and append to tempi-array. 
    Calculate the duration of a whole note to later on define the values of the other notes
    """
    global dauer
    
    dauer = 0.0
    counter = 1

    for x in midi_data.get_tempo_changes(): #pretty_midi saves the tempo of a midi-file in nested-arrays, therefore a few for-loops and if statements are necessary
        for e in x:
            if e > 0:
                if counter > 0:
                    tempi.append(round(e))
                    counter = 0
                    break
    
    dauer = 60000/(e/4)

def createTempoArray():
    """Write the tempi-struct into the header-file
    """
    file2write.write("int tempi[] = {")

    for t in tempi: #iterates through tempi-array and filles the array with elements
        if t > 40:
            file2write.write(str(t))
            file2write.write(",")
    file2write.write("};\n\n")


def createSongsArray():
    """Writes the note-struct into the header-file
    """
    file2write.write("unsigned short songs[5][2500][2] = {")

def fillSongsArray():
    """Calculates the duration and pitch of notes.
    Writes the struct into the header-file
    """
    counter = 1
    notealt = 0.0
    frequenz = 0
    notencounter = 0

    file2write.write("\n{")
    for instrument in midi_data.instruments:
        while counter == 1:#first line of the instrument e.g piano it will only save the treble clef and NOT the bass clef
            for note in instrument.notes:
                if note.start - notealt >= 0.15: #If the note is a break it will save it as such
                    value = dauer/((note.start - notealt)*1000)
                    y = round(value)
                    file2write.write("{0,")
                    file2write.write(str(y+1))
                    file2write.write("},")

                else:
                    frequenz = int(pretty_midi.note_number_to_hz(note.pitch)) #convert the midi-note-number to a frequency with function of the library
                    value = dauer/((note.end - note.start)*1000) #calculates the duration of the note
                    x = round(value)
                    file2write.write("{")
                    file2write.write(str(frequenz))
                    file2write.write(",")
                    file2write.write(str(x))
                    file2write.write("},")
                notealt = note.end
            counter += 1
            file2write.write("},")
            #file2write.write("};\n")

def closeHFile():
    """Close the header-file
    """
    file2write.close()


def main():
    """Execute functions in order.
    
    """
    global i, tempi
    
    i = 0
    tempi = []

    getSongNames()
    openHFile()
    createSongsArray()
    while i <= len(namen)-1: #global iteration
        openMidi()
        getTempo()
        fillSongsArray()
        i += 1
    file2write.write("};\n")
    createTempoArray()
    closeHFile()
    
    print("Done!") #If code executed successfully print Done!
    

if __name__ == '__main__':
    main() 

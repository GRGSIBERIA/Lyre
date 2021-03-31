#include "midisequence.h"

void GenerateToToneKeyboardBinding(std::unordered_map<int, int>& dvorakToTone, std::unordered_map<int, int>& qwertyToTone)
{
	dvorakToTone[187] = 0;	// ;
	dvorakToTone[79] = 1;	// o
	dvorakToTone[81] = 2;	// q
	dvorakToTone[69] = 3;	// .
	dvorakToTone[74] = 4;	// j
	dvorakToTone[85] = 5;	// u
	dvorakToTone[75] = 6;	// k
	dvorakToTone[66] = 7;	// b
	dvorakToTone[0x48] = 8;	// h
	dvorakToTone[0x4d] = 9;	// m
	dvorakToTone[0x54] = 10;	// t
	dvorakToTone[0x57] = 11;	// v
	dvorakToTone[0x4e] = 12;	// s
	dvorakToTone[0x56] = 13;		// z bhmtwnv

	qwertyToTone['z'] = 0;
	qwertyToTone['s'] = 1;
	qwertyToTone['x'] = 2;
	qwertyToTone['d'] = 3;
	qwertyToTone['c'] = 4;
	qwertyToTone['f'] = 5;
	qwertyToTone['v'] = 6;
	qwertyToTone['n'] = 7;
	qwertyToTone['j'] = 8;
	qwertyToTone['m'] = 9;
	qwertyToTone['k'] = 10;
	qwertyToTone[188] = 11;
	qwertyToTone['l'] = 12;
	qwertyToTone[190] = 13;
}

void MakeSound(HMIDIOUT hMidiOut, int toneNumber, int velocity)
{
	static DWORD prevMsg = -1;

	if (prevMsg != -1)
	{
		prevMsg -= 0x10;
		midiOutShortMsg(hMidiOut, prevMsg);
	}

	DWORD msg = (velocity & 0xFF) << 16 | (toneNumber & 0xFF) << 8 | 0x90;
	prevMsg = msg;

	UINT result = midiOutShortMsg(hMidiOut, msg);
}

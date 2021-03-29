#include "midisequence.h"

void GenerateToToneKeyboardBinding(std::unordered_map<int, int>& dvorakToTone, std::unordered_map<int, int>& qwertyToTone)
{
	dvorakToTone[187] = 0;
	dvorakToTone[79] = 1;
	dvorakToTone[81] = 2;
	dvorakToTone[69] = 3;
	dvorakToTone[74] = 4;
	dvorakToTone[85] = 5;
	dvorakToTone[75] = 6;
	dvorakToTone[66] = 7;
	dvorakToTone[68] = 8;
	dvorakToTone[72] = 9;
	dvorakToTone[77] = 10;
	dvorakToTone[87] = 11;
	dvorakToTone[78] = 12;
	dvorakToTone[90] = 13;

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

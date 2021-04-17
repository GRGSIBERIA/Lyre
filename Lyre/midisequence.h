#pragma once
#include <unordered_map>
#include <Windows.h>
#include <mmsystem.h>

void GenerateToToneKeyboardBinding(std::unordered_map<int, int>& dvorakToTone, std::unordered_map<int, int>& qwertyToTone);

void MakeSound(HMIDIOUT hMidiOut, int toneNumber, int velocity);
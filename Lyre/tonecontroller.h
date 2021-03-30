#pragma once
#include <array>

class ToneController
{
	int basicTone = 0x2c;

	int key = 0;

	bool isMinor = false;

	const std::array<int, 7> toneSequence = { 0, 2, 4, 5, 7, 9, 11 };

public:
	ToneController();

	virtual ~ToneController();

	void KeyChange(const int num);

	const int GetTone(const int keyboardHitNum, const int leftShift, const int rightShift) const;
};
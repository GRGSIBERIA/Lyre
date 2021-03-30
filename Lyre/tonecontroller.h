#pragma once

class ToneController
{
	int basicTone = 0x2c;

	int key = 0;

public:
	ToneController();

	virtual ~ToneController();

	void KeyChange(const int num);
};
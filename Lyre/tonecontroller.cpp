#include "tonecontroller.h"

ToneController::ToneController()
{
}

ToneController::~ToneController()
{
}

void ToneController::KeyChange(const int num)
{
	// 4bitまでがキー
	// 5bit目はメジャーマイナー
	int key = num & 0b1111;
	int minor = num & 0b10000;

	this->isMinor = minor > 0;
	this->key = key;
}

const int ToneController::GetTone(const int keyboardHitNum, const int leftShift, const int rightShift) const
{
	int mod = keyboardHitNum % 7;
	int octave = keyboardHitNum / 7;

	if (leftShift > 0 && rightShift > 0)
	{
		octave += 2;
	}
	else
	{
		octave -= leftShift > 0 ? 1 : 0;
		octave += rightShift > 0 ? 1 : 0;
	}

	int tone = toneSequence[mod];
	int minor = isMinor ? -3 : 0;
	
	// 0x2c(C3) + 0x02(Dmaj) + 0x04(3rd) + 0x00(maj) + 0x00(O1) * 12
	// 0x2e + 0x04 = 0x32
	return basicTone + key + tone + isMinor + octave * 12;
}

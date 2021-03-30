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

	if (minor > 0) key -= 3;	// マイナーキーに変更

	this->key = key;
}

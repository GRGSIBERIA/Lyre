#include "tonecontroller.h"

ToneController::ToneController()
{
}

ToneController::~ToneController()
{
}

void ToneController::KeyChange(const int num)
{
	// 4bit�܂ł��L�[
	// 5bit�ڂ̓��W���[�}�C�i�[
	int key = num & 0b1111;
	int minor = num & 0b10000;

	if (minor > 0) key -= 3;	// �}�C�i�[�L�[�ɕύX

	this->key = key;
}

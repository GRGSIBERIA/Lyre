#pragma once
#include <unordered_map>
#include <Windows.h>
#include <mmsystem.h>

#include "tonecontroller.h"

/******************************************************************
 * グローバル変数の宣言
 ******************************************************************/

HDC hBackDC = NULL;			//!< バックバッファ
HBITMAP hBackBitmap = NULL;	//!< バックバッファのビットマップ領域
bool dvorakMode = false;	//!< Dvorakモードの有無

std::unordered_map<int, int> dvorakToTone;
std::unordered_map<int, int> qwertyToTone;
HMIDIOUT hMidiOut;

ToneController controller;
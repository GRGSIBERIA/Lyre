#include <windows.h>
#include <mmeapi.h>
#include <mmsystem.h>

/******************************************************************
 * 関数の前方宣言
 ******************************************************************/

LRESULT CALLBACK WndProc(
	HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

void CenteringWindow(HWND& hwnd);

void CreateBuffer(HWND hwnd);

void Render(HWND hwnd);

/******************************************************************
 * グローバル変数の宣言
 ******************************************************************/

HDC hBackDC = NULL;			//!< バックバッファ
HBITMAP hBackBitmap = NULL;	//!< バックバッファのビットマップ領域
bool dvorakMode = false;	//!< Dvorakモードの有無
HMIDIOUT hMidiOut;

int WINAPI WinMain(
	HINSTANCE hInstance, HINSTANCE hPrevInstance,
	LPSTR lpszCmdLine, int nCmdShow)
{
	TCHAR appName[] = TEXT("Lyre in the sky");
	WNDCLASS wc;
	HWND hwnd;
	MSG msg;
	MIDIHDR header;
	BYTE GMSystemOn[] = { 0xf0, 0x7e, 0x7f, 0x09, 0x01, 0xf7 };

	wc.style = CS_HREDRAW | CS_VREDRAW;
	wc.lpfnWndProc = WndProc;
	wc.cbClsExtra = 0;
	wc.cbWndExtra = 0;
	wc.hInstance = hInstance;
	wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
	wc.lpszMenuName = NULL;
	wc.lpszClassName = appName;

	if (!RegisterClass(&wc)) return 0;

	hwnd = CreateWindow(
		appName, TEXT("Lyre in the sky"),
		WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT, CW_USEDEFAULT,
		CW_USEDEFAULT, CW_USEDEFAULT,
		NULL, NULL,
		hInstance, NULL);

	if (!hwnd) return 0;

	midiOutOpen(&hMidiOut, MIDI_MAPPER, 0, 0, 0);

	/* GMシステムオン */
	ZeroMemory(&header, sizeof(MIDIHDR));
	header.lpData = (LPSTR)GMSystemOn;
	header.dwBufferLength = sizeof(GMSystemOn);
	header.dwFlags = 0;

	/* GM音源で鳴らすように指示を出す */
	//midiOutPrepareHeader(hMidiOut, &header, sizeof(MIDIHDR));
	//midiOutLongMsg(hMidiOut, &header, sizeof(MIDIHDR));
	//midiOutUnprepareHeader(hMidiOut, &header, sizeof(MIDIHDR));

	/* ハープの音色を使用 */
	//midiOutShortMsg(hMidiOut, 0x00002ec0);

	midiOutShortMsg(hMidiOut, 0x007f3c80);

	ZeroMemory(&msg, sizeof(msg));
	while (msg.message != WM_QUIT)
	{
		if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
		else
			Render(hwnd);
	}

	midiOutReset(hMidiOut);
	midiOutClose(hMidiOut);

	return msg.wParam;
}

LRESULT CALLBACK WndProc(
	HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	switch (uMsg)
	{
	case WM_CREATE:
		CenteringWindow(hwnd);
		CreateBuffer(hwnd);
		return 0;

	case WM_KEYDOWN:
		switch (wParam)
		{
		case VK_ESCAPE:
			dvorakMode = !dvorakMode;
			break;
		case VK_LSHIFT:
			break;
		case VK_RSHIFT:
			break;
		default:
			break;
		}

		InvalidateRect(hwnd, NULL, FALSE);
		return 0;

	case WM_DESTROY:
		DeleteDC(hBackDC);
		DeleteObject(hBackBitmap);
		PostQuitMessage(0);
		return 0;
	}

	return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

void CenteringWindow(HWND& hwnd)
{
	const int W = 640;
	const int H = 480;
	const int dispW = GetSystemMetrics(SM_CXSCREEN);
	const int dispH = GetSystemMetrics(SM_CYSCREEN);

	SetWindowPos(hwnd, NULL,
		(dispW - W) >> 1, (dispH - H) >> 1,
		W, H, SWP_SHOWWINDOW);
}

/**
 * バックバッファの生成と初期化
 */
void CreateBuffer(HWND hwnd)
{
	HDC hdc;
	hdc = GetDC(hwnd);
	hBackDC = CreateCompatibleDC(hdc);
	hBackBitmap = CreateCompatibleBitmap(hdc, 640, 480);
	SelectObject(hBackDC, hBackBitmap);
	ReleaseDC(hwnd, hdc);
}

void Render(HWND hwnd)
{
	HDC hdc;
	RECT client;

	LPCTSTR enableDvorak = TEXT("DVORAK MODE");
	LPCTSTR disableDvorak = TEXT("QWERTY MODE");

	// 背景色で塗りつぶし
	GetClientRect(hwnd, &client);
	FillRect(hBackDC, &client, (HBRUSH)GetStockObject(WHITE_BRUSH));

	if (dvorakMode)
		TextOut(hBackDC, 10, 10, enableDvorak, lstrlen(enableDvorak));
	else
		TextOut(hBackDC, 10, 10, disableDvorak, lstrlen(disableDvorak));

	hdc = GetDC(hwnd);
	BitBlt(
		hdc, 0, 0, 
		client.right - client.left, 
		client.bottom - client.top, 
		hBackDC, 0, 0, SRCCOPY);
	ReleaseDC(hwnd, hdc);
}

#include <windows.h>
#include <mmeapi.h>

LRESULT CALLBACK WndProc(
	HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

void CenteringWindow(HWND& hwnd);

int WINAPI WinMain(
	HINSTANCE hInstance, HINSTANCE hPrevInstance,
	LPSTR lpszCmdLine, int nCmdShow)
{
	TCHAR appName[] = TEXT("Lyre in the sky");
	WNDCLASS wc;
	HWND hwnd;
	MSG msg;
	HMIDIOUT hMidiOut;

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
	midiOutShortMsg(hMidiOut, 0x007f3c90);

	while (GetMessage(&msg, NULL, 0, 0) > 0)
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}

	midiOutReset(hMidiOut);
	midiOutClose(hMidiOut);

	return msg.wParam;
}

LRESULT CALLBACK WndProc(
	HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	HDC hdc;
	PAINTSTRUCT ps;

	switch (uMsg)
	{
	case WM_CREATE:
		CenteringWindow(hwnd);
		return 0;

	case WM_PAINT:
		hdc = BeginPaint(hwnd, &ps);
		RECT client;

		// 白いブラシを選択
		SelectObject(hdc, GetStockObject(WHITE_BRUSH));
		
		// 矩形で塗りつぶし
		GetClientRect(hwnd, &client);
		Rectangle(hdc, 0, 0, client.right, client.bottom);
		EndPaint(hwnd, &ps);

	case WM_KEYDOWN:
		hdc = GetDC(hwnd);
		TextOut(hdc, 10, 10, (PTSTR)&wParam, 1);
		ReleaseDC(hwnd, hdc);
		return 0;

	case WM_DESTROY:
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

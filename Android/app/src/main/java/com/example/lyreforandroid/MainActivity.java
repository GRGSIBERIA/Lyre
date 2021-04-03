package com.example.lyreforandroid;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.Button;

import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioTrack;

import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity {

    private Button[] toneButtons;
    private Button[] keyButtons;
    private AudioTrack[] tracks;
    private int selectedKey;
    private int[] scale;
    private boolean isMajor;

    final int SamplingRate = 48000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        isMajor = true;
        selectedKey = 0;

        scale = new int[] {
            0, 2, 4, 5, 7, 9, 11
        };

        toneButtons = new Button[] {
                findViewById(R.id.button11),
                findViewById(R.id.button12),
                findViewById(R.id.button13),
                findViewById(R.id.button14),
                findViewById(R.id.button15),
                findViewById(R.id.button16),
                findViewById(R.id.button17),
                findViewById(R.id.button21),
                findViewById(R.id.button22),
                findViewById(R.id.button23),
                findViewById(R.id.button24),
                findViewById(R.id.button25),
                findViewById(R.id.button26),
                findViewById(R.id.button27),
                findViewById(R.id.button31),
                findViewById(R.id.button32),
                findViewById(R.id.button33),
                findViewById(R.id.button34),
                findViewById(R.id.button35),
                findViewById(R.id.button36),
                findViewById(R.id.button37)
        };

        keyButtons = new Button[] {
                findViewById(R.id.buttonC),
                findViewById(R.id.buttonCs),
                findViewById(R.id.buttonD),
                findViewById(R.id.buttonDs),
                findViewById(R.id.buttonE),
                findViewById(R.id.buttonF),
                findViewById(R.id.buttonFs),
                findViewById(R.id.buttonG),
                findViewById(R.id.buttonGs),
                findViewById(R.id.buttonA),
                findViewById(R.id.buttonAs),
                findViewById(R.id.buttonB)
        };

        Button isMajorBtn = findViewById(R.id.isMinor);
        isMajorBtn.setOnClickListener(v -> {
            isMajor = !isMajor;
        });
        isMajorBtn.setSoundEffectsEnabled(false);

        for (int i = 0; i < toneButtons.length; ++i)
        {
            int finalI = i;
            toneButtons[i].setOnClickListener(v -> {
                wavPlay(finalI);
            });
            toneButtons[i].setSoundEffectsEnabled(false);
        }

        for (int i = 0; i < keyButtons.length; ++i)
        {
            int finalI = i;
            keyButtons[i].setOnClickListener(v -> {
                selectedKey = finalI;
            });
            keyButtons[i].setSoundEffectsEnabled(false);
        }

        tracks = new AudioTrack[] {
                BuildTrack(R.raw.a21),  // A0
                BuildTrack(R.raw.a22),
                BuildTrack(R.raw.a23),
                BuildTrack(R.raw.a24),  // C1
                BuildTrack(R.raw.a25),
                BuildTrack(R.raw.a26),
                BuildTrack(R.raw.a27),
                BuildTrack(R.raw.a28),
                BuildTrack(R.raw.a29),
                BuildTrack(R.raw.a30),
                BuildTrack(R.raw.a31),
                BuildTrack(R.raw.a32),
                BuildTrack(R.raw.a33),
                BuildTrack(R.raw.a34),
                BuildTrack(R.raw.a35),
                BuildTrack(R.raw.a36),  // C2
                BuildTrack(R.raw.a37),
                BuildTrack(R.raw.a38),
                BuildTrack(R.raw.a39),
                BuildTrack(R.raw.a40),
                BuildTrack(R.raw.a41),
                BuildTrack(R.raw.a42),
                BuildTrack(R.raw.a43),
                BuildTrack(R.raw.a44),
                BuildTrack(R.raw.a45),
                BuildTrack(R.raw.a46),
                BuildTrack(R.raw.a47),
                BuildTrack(R.raw.a48),  // C3
                BuildTrack(R.raw.a49),
                BuildTrack(R.raw.a50),
                BuildTrack(R.raw.a51),
                BuildTrack(R.raw.a52),
                BuildTrack(R.raw.a53),
                BuildTrack(R.raw.a54),
                BuildTrack(R.raw.a55),
                BuildTrack(R.raw.a56),
                BuildTrack(R.raw.a57),
                BuildTrack(R.raw.a58),
                BuildTrack(R.raw.a59),
                BuildTrack(R.raw.a60),  // C4
                BuildTrack(R.raw.a61),
                BuildTrack(R.raw.a62),
                BuildTrack(R.raw.a63),
                BuildTrack(R.raw.a64),
                BuildTrack(R.raw.a65),
                BuildTrack(R.raw.a66),
                BuildTrack(R.raw.a67),
                BuildTrack(R.raw.a68),
                BuildTrack(R.raw.a69),
                BuildTrack(R.raw.a70),
                BuildTrack(R.raw.a71)   // B4
        };
    }

    // AudioTrackを使うとSoundPoolよりも低レイテンシで再生できるらしい
    // https://akira-watson.com/android/audiotrack.html
    private AudioTrack BuildTrack(int resourceId)
    {
        InputStream input = null;
        byte[] wavData = null;

        try
        {
            input = getResources().openRawResource(resourceId);
            wavData = new byte[input.available()];
            input.read(wavData);
        }
        catch (IOException ioe)
        {
            ioe.printStackTrace();
            return null;
        }

        // バッファサイズを取得
        /* MODE_STATICの場合はバッファをストリーミングせずにリソースを使い回す
        int bufSize = android.media.AudioTrack.getMinBufferSize(
                SamplingRate, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT
        );
        */

        AudioTrack track = new AudioTrack.Builder()
                .setAudioAttributes(new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_GAME)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                        .build())
                .setAudioFormat(new AudioFormat.Builder()
                        .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                        .setSampleRate(SamplingRate)
                        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                        .build())
                .setBufferSizeInBytes(wavData.length - 44)
                .setTransferMode(AudioTrack.MODE_STATIC)
                .build();

        // data+4バイト目以降の数百バイトが0xFFFFになって不安定
        wavData[802] = 0; wavData[803] = 0;
        wavData[wavData.length - 2] = 0; wavData[wavData.length - 1] = 0;

        track.write(wavData, 802, wavData.length - 802);

        return track;
    }

    private void wavPlay(int num)
    {
        int majorUp = isMajor ? 3 : 0;

        int toneId = selectedKey + majorUp + scale[num % 7] + (int)(num / 7) * 12;

        tracks[toneId].stop();
        tracks[toneId].play();
    }
}
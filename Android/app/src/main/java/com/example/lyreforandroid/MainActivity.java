package com.example.lyreforandroid;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;

import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioTrack;

import java.io.IOException;
import java.io.InputStream;

public class MainActivity extends AppCompatActivity {

    private Button[] toneButtons;
    private Button[] octaveButtons;
    private AudioTrack[] tracks;
    private int selectedOctave;

    final int SamplingRate = 48000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        toneButtons = new Button[] {
                findViewById(R.id.button1),
                findViewById(R.id.button2),
                findViewById(R.id.button3),
                findViewById(R.id.button4),
                findViewById(R.id.button5),
                findViewById(R.id.button6),
                findViewById(R.id.button7)
        };

        octaveButtons = new Button[] {
                findViewById(R.id.buttonOctave1),
                findViewById(R.id.buttonOctave2),
                findViewById(R.id.buttonOctave3)
        };

        for (int i = 0; i < toneButtons.length; ++i)
        {
            int finalI = i;
            toneButtons[i].setOnClickListener(v -> {
                wavPlay(finalI);
            });
        }

        for (int i = 0; i < octaveButtons.length; ++i)
        {
            int finalI = i;
            octaveButtons[i].setOnClickListener(v -> {
                selectedOctave = finalI;
            });
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
        int bufSize = android.media.AudioTrack.getMinBufferSize(
                SamplingRate, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT
        );

        AudioTrack track = new AudioTrack.Builder()
                .setAudioAttributes(new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_GAME)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                        .build())
                .setAudioFormat(new AudioFormat.Builder()
                        .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                        .setSampleRate(48000)
                        .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                        .build())
                .setBufferSizeInBytes(bufSize)
                .build();

        track.write(wavData, 44, wavData.length - 44);

        return track;
    }

    private void wavPlay(int num)
    {

    }
}
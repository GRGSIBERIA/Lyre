package com.example.lyreforandroid;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;

import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioTrack;

public class MainActivity extends AppCompatActivity {

    private Button[] toneButtons;
    private AudioTrack[] tracks;

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

        for (int i = 0; i < toneButtons.length; ++i)
        {
            int finalI = i;
            toneButtons[i].setOnClickListener(v -> {
                wavPlay(finalI);
            });
        }


    }

    // AudioTrackを使うとSoundPoolよりも低レイテンシで再生できるらしい
    // https://akira-watson.com/android/audiotrack.html
    private AudioTrack BuildTrack(int num)
    {
        final int bufferSize = 0;

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
                .setBufferSizeInBytes(bufferSize)
                .build();

        return track;
    }

    private void wavPlay(int num)
    {

    }
}
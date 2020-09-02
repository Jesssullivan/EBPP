// webgl_float_test.ts
import {audio_model, audio_utils, spectrogram_utils} from '../src/index';

// a default, hardcoded waveform snippet to try from different devices:
const testWaveform = require('./test_waveform.json');

// `test_array` here stands in for what would usually be a
//  waveform we just recorded out of a Blob:
const test_array = new Float32Array(testWaveform.length);

for (let i = 0; i < testWaveform.length; i++){
    test_array[i] = testWaveform[i];
}

/* tslint:disable:prefer-const */
const webglButton = document.getElementById("webglButton") as HTMLButtonElement;
const testButton = document.getElementById("testButton") as HTMLButtonElement;
const canvas = document.querySelector('.visualizer') as HTMLCanvasElement;
const mainSection = document.querySelector('.container-fluid') as HTMLDivElement;
let imgCrop = document.createElement('img');
/* tslint:enable:prefer-const */

// Spectrogram Visualization Parameters
const targetSampleRate = 22050;
const stftWindowSeconds = 0.015;
const stftHopSeconds = 0.005;
const topDB = 80;

const MODEL_URL = 'models/audio/model.json';
const LABELS_URL = 'models/audio/labels.json';

const merlinAudio = new audio_model.MerlinAudioModel(LABELS_URL, MODEL_URL);

function updateVis() {

    // visualize the cropped sample
    const dbSpec = generateSpectrogram(test_array); //audio_utils.dBSpectrogram(audioData.waveform, spec_params);
    const cropped_imageURI = spectrogram_utils.dBSpectrogramToImage(dbSpec, topDB);

    // create / update cropped visualization
    const cropped_height = 300;
    const cropped_width = Math.round(dbSpec.length);

    imgCrop.src = cropped_imageURI;
    imgCrop.height = cropped_height;
    imgCrop.width =  cropped_width;

    const specCropImage = document.getElementById('specCropHolder');
    while (specCropImage!.firstChild) {
        specCropImage!.removeChild(specCropImage!.firstChild);
    }

    specCropImage!.appendChild(imgCrop);

    return test_array;

}

async function averageClassifyWaveform(waveform : Float32Array) {

    const result = await merlinAudio.averagePredictV3(waveform, targetSampleRate);
    const labels = result[0] as string[];
    const scores = result[1] as Float32Array;

    return [labels, scores];

}

function generateSpectrogram(waveform : Float32Array) : Float32Array[]{

    const window_length_samples = Math.round(targetSampleRate * stftWindowSeconds);
    const hop_length_samples = Math.round(targetSampleRate * stftHopSeconds);
    const fft_length = Math.pow(2, Math.ceil(Math.log(window_length_samples) / Math.log(2.0)));

    const spec_params = {
        sampleRate: targetSampleRate,
        hopLength: hop_length_samples,
        winLength: window_length_samples,
        nFft: fft_length,
        topDB
    };

    return audio_utils.dBSpectrogram(waveform, spec_params);

}

webglButton.onclick = () => {

    // benefit of the doubt here, ideally client is on a `proper` browser:
    const gl = canvas.getContext('webgl');

    // we'll return our findings to a placeholder element:
    const glSupportHolderEl = document.getElementById('glSupportHolder');
    while (glSupportHolderEl!.firstChild) {
        glSupportHolderEl!.removeChild(glSupportHolderEl!.firstChild);
    }

    const prec = gl!.getShaderPrecisionFormat(gl!.VERTEX_SHADER, gl!.HIGH_FLOAT)!.precision;

    if (prec >= 23) {
        glSupportHolderEl!.prepend("this device's shader precision is " +
            prec.toString() +
            ", and should be able to handle float32 webgl values.");

    } else {
        glSupportHolderEl!.prepend("this device' shader precision is " + prec.toString() +
            ", and should may not represent float32 values :(");

    }

};

testButton.onclick = () => {

    updateVis();

    const sampleHolderEl = document.getElementById('specSampleHolder');
    while (sampleHolderEl!.firstChild) {
        sampleHolderEl!.removeChild(sampleHolderEl!.firstChild);
    }

    averageClassifyWaveform(test_array).then(([labels, scores]) => {

        const resultEl = document.createElement('ul');

        for (let i = 0; i < 10; i++) {
            const scoreEl = document.createElement('li');
            scoreEl.textContent = labels[i] + " " + scores[i];
            resultEl.appendChild(scoreEl);
            sampleHolderEl!.prepend(resultEl);

        }

    });
};

// Make the canvas the full width
window.addEventListener('resize', () => {
    canvas.width = mainSection.offsetWidth;
});

window.dispatchEvent(new Event('resize'));
import * as ort from "onnxruntime-web/wasm";
import wasmUrl from "../node_modules/onnxruntime-web/dist/ort-wasm-simd-threaded.wasm?url";
ort.env.wasm.wasmPaths = { wasm: wasmUrl };
ort.env.wasm.numThreads = 1;
export const features = ["bekleme_sn", "degistirme_sayisi", "ipucu_sayisi"];
let session, config;
export async function loadModel() {
  const base = import.meta.env.BASE_URL;
  const manifest = await fetch(`${base}model/source.json`).then((r) => {
    if (!r.ok) throw Error("Model henüz hazırlanmadı");
    return r.json();
  });
  let root = `${base}model/`;
  if (manifest.repo) {
    if (!/^[a-f0-9]{40}$/.test(manifest.commit))
      throw Error("Sabit HF commit gerekli");
    root = `https://huggingface.co/${manifest.repo}/resolve/${manifest.commit}/`;
  }
  config = await fetch(`${root}config.json`).then((r) => r.json());
  if (
    JSON.stringify(config.features.map((f) => f.name)) !==
      JSON.stringify(features) ||
    config.classes.join() !== "kisa,ayrintili" ||
    config.input_name !== "features"
  )
    throw Error("Model sözleşmesi uyuşmuyor");
  session = await ort.InferenceSession.create(`${root}model.onnx`, {
    executionProviders: ["wasm"],
  });
  return config;
}
export async function predict(values) {
  if (!session) throw Error("Model hazır değil");
  if (
    values.length !== 3 ||
    values.some((v, i) => !Number.isFinite(v) || v < 0 || v > [300, 20, 10][i])
  )
    throw Error("Geçersiz model girdisi");
  const output = await session.run({
    features: new ort.Tensor("float32", Float32Array.from(values), [1, 3]),
  });
  return Number(output.probabilities.data[1]);
}

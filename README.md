## REVISION: Rendering Tools Enable Spatial Fidelity in Vision-Language Models

<p align="center">
    📃 <a href="https://arxiv.org/abs/2408.02231/" target="_blank">Paper</a> |
    🎮 <a href="https://agneetchatterjee.com/revision/" target="_blank">Project Website</a>
</p>

## 📄 Abstract
_Text-to-Image (T2I) and multimodal large language models (MLLMs) have been adopted in solutions for several computer vision and multimodal learning tasks. 
  However, it has been found that such vision-language models lack the ability to correctly reason over spatial relationships. 
  To tackle this shortcoming, we develop the REVISION framework which improves spatial fidelity in vision-language models. 
  REVISION is a 3D rendering based pipeline that generates spatially accurate synthetic images, given a textual prompt. 
REVISION is an extendable framework, which currently supports 100+ 3D assets, 11 spatial relationships, all with diverse camera perspectives and backgrounds. Leveraging images from REVISION as additional guidance in a training-free manner consistently improves the spatial consistency of T2I models across all spatial relationships, achieving competitive performance on the VISOR and T2I-CompBench benchmarks. 
We also design RevQA, a question-answering benchmark to evaluate the spatial reasoning abilities of MLLMs, and find that state-of-the-art models are not robust to complex spatial reasoning under adversarial settings. Our results and findings indicate that utilizing rendering-based frameworks is an effective approach for developing spatially-aware generative models._


## 📚 Contents

- [Data](#data)
- [Sample Scripts](#scripts)
- [Citing](#citing)
- [Acknowledgments](#ack)

<a name="data"></a>
## 🖼️ Data

Please refer to the [REVISION](https://huggingface.co/revision-t2i) organization on Hugging Face 🤗.

<a name="scripts"></a>
## 📊 Sample Scripts

```inference.py``` presents a simple script that can be modified based on the input prompt and a REVISION image.

<a name="citing"></a>
## 📜 Citing

```bibtex
@misc{chatterjee2024revisionrenderingtoolsenable,
      title={REVISION: Rendering Tools Enable Spatial Fidelity in Vision-Language Models}, 
      author={Agneet Chatterjee and Yiran Luo and Tejas Gokhale and Yezhou Yang and Chitta Baral},
      year={2024},
      eprint={2408.02231},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2408.02231}, 
}
```

<a name="ack"></a>
## 🙏 Acknowledgments

The authors acknowledge resources and support from the Research Computing facilities at Arizona State University. This work was supported by NSF RI grants \#1750082 and \#2132724. The views and opinions of the authors expressed herein do not necessarily state or reflect those of the funding agencies and employers. 

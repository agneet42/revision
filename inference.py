from diffusers import AutoPipelineForImage2Image, AutoPipelineForText2Image
from PIL import Image
import torch 

prompt = "a tv on the left of a fish"

pipeline_text2image = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
).to("cuda") # any T2I model 

pipeline = AutoPipelineForImage2Image.from_pipe(pipeline_text2image).to("cuda")

revision_image = 'assets/a_tv_on_the_left_of_a_fish_revision.png' # image from REVISION
revision_image = Image.open(revision_image)

prompt+=' van gogh style'
generator = torch.Generator(device='cuda').manual_seed(51)
image = pipeline(prompt=prompt, image=revision_image, generator=generator, strength=0.7, guidance_scale=7.5).images
image[0].save("assets/%s.png"%(prompt.replace(' ', '_')))
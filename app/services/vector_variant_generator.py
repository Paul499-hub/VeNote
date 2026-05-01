from app.ai_models.model_registry import vv_model, vv_tokenizer

class VectorVariantGeneratorService():
    def __init__(self):
        pass

    def msg_ai(self, msg:str):
        messages = [{"role":"user", "content":msg}]
        text = vv_tokenizer.apply_chat_template(
            messages, 
            tokenize=False,
            add_generation_prompt=True,
        )
        input_device = next(vv_model.parameters()).device
        ai_input = vv_tokenizer(text, return_tensors="pt").to(input_device)
        out = vv_model.generate(
            **ai_input,
            max_new_tokens=128
        )
        new_tokens = out[0][ai_input["input_ids"].shape[1]:]
        ai_resp = vv_tokenizer.decode(new_tokens, skip_special_tokens=True)
        return f"[input_device={input_device}]: {ai_resp}"
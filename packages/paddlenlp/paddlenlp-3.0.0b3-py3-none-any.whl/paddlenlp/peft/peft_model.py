# from __future__ import annotations

# import collections
# import copy
# import inspect
# import os
# import warnings
# from contextlib import contextmanager, nullcontext
# from copy import deepcopy
# from dataclasses import dataclass
# from typing import Any, Literal, Optional, Union

# import packaging.version
# import paddle
# import transformers
# from accelerate import dispatch_model, infer_auto_device_map, init_empty_weights
# from accelerate.hooks import AlignDevicesHook, add_hook_to_module, remove_hook_from_submodules
# from accelerate.utils import get_balanced_memory, named_module_tensors
# from huggingface_hub import HfFileSystem, ModelCard, ModelCardData, hf_hub_download
# from safetensors import safe_open
# from safetensors.numpy import save_file as safe_save_file
# from paddle.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss
# from transformers import Cache, DynamicCache, EncoderDecoderCache, PreTrainedModel
# from transformers.modeling_outputs import QuestionAnsweringModelOutput, SequenceClassifierOutput, TokenClassifierOutput
# from transformers.utils import PushToHubMixin

# from peft.utils.constants import DUMMY_MODEL_CONFIG, PEFT_TYPE_TO_PREFIX_MAPPING

# from . import __version__
# from .config import PeftConfig
# from .tuners import (
#     AdaLoraModel,
#     AdaptionPromptModel,
#     BOFTModel,
#     BoneModel,
#     CPTEmbedding,
#     FourierFTModel,
#     HRAModel,
#     IA3Model,
#     LNTuningModel,
#     LoHaModel,
#     LoKrModel,
#     LoraModel,
#     MultitaskPromptEmbedding,
#     OFTModel,
#     PolyModel,
#     PrefixEncoder,
#     PromptEmbedding,
#     PromptEncoder,
#     VBLoRAModel,
#     VeraModel,
#     XLoraConfig,
#     XLoraModel,
# )
# from .tuners.tuners_utils import BaseTuner, BaseTunerLayer
# from .utils import (
#     SAFETENSORS_WEIGHTS_NAME,
#     TRANSFORMERS_MODELS_TO_PREFIX_TUNING_POSTPROCESS_MAPPING,
#     WEIGHTS_NAME,
#     PeftType,
#     TaskType,
#     _get_batch_size,
#     _prepare_prompt_learning_config,
#     _set_adapter,
#     _set_trainable,
#     get_peft_model_state_dict,
#     id_tensor_storage,
#     infer_device,
#     load_peft_weights,
#     map_cache_to_layer_device_map,
#     set_peft_model_state_dict,
#     shift_tokens_right,
# )


# PEFT_TYPE_TO_MODEL_MAPPING = {
#     PeftType.LORA: LoraModel,
#     PeftType.LOHA: LoHaModel,
#     PeftType.LOKR: LoKrModel,
#     PeftType.PROMPT_TUNING: PromptEmbedding,
#     PeftType.P_TUNING: PromptEncoder,
#     PeftType.PREFIX_TUNING: PrefixEncoder,
#     PeftType.ADALORA: AdaLoraModel,
#     PeftType.BOFT: BOFTModel,
#     PeftType.ADAPTION_PROMPT: AdaptionPromptModel,
#     PeftType.IA3: IA3Model,
#     PeftType.OFT: OFTModel,
#     PeftType.POLY: PolyModel,
#     PeftType.LN_TUNING: LNTuningModel,
#     PeftType.VERA: VeraModel,
#     PeftType.FOURIERFT: FourierFTModel,
#     PeftType.XLORA: XLoraModel,
#     PeftType.HRA: HRAModel,
#     PeftType.VBLORA: VBLoRAModel,
#     PeftType.CPT: CPTEmbedding,
#     PeftType.BONE: BoneModel,
# }




# from .lokr import LoKrConfig, LoKrModel
# from .lora import LoRAConfig, LoRAModel
# from .prefix import PrefixConfig, PrefixModelForCausalLM
# from .reft import ReFTModel
# from .vera import VeRAConfig, VeRAModel




# def create_peft_model(model_args, reft_args, training_args, dtype, model_config, model, reft_layers):
#     if model_args.prefix_tuning:
#         if training_args.pipeline_parallel_degree > 1:
#             raise NotImplementedError("Prefix tuning is not implemented for pipeline parallelism.")

#         prefix_tuning_params = get_prefix_tuning_params(model)
#         prefix_config = PrefixConfig(
#             num_prefix_tokens=model_args.num_prefix_tokens,
#             num_attention_heads=prefix_tuning_params["num_attention_heads"],
#             num_hidden_layers=prefix_tuning_params["num_hidden_layers"],
#             hidden_size=prefix_tuning_params["hidden_size"],
#             multi_query_group_num=prefix_tuning_params["multi_query_group_num"],
#             dtype=dtype,
#         )
#         if model_args.prefix_path is None:
#             model = PrefixModelForCausalLM(
#                 model=model,
#                 prefix_config=prefix_config,
#                 postprocess_past_key_value=prefix_tuning_params["postprocess_past_key_value"],
#             )
#         else:
#             model = PrefixModelForCausalLM.from_pretrained(
#                 model=model,
#                 prefix_path=model_args.prefix_path,
#                 postprocess_past_key_value=prefix_tuning_params["postprocess_past_key_value"],
#             )
#         model.print_trainable_parameters()

#     if model_args.lora:
#         if training_args.sharding_parallel_degree > 1:
#             assert (
#                 "enable_stage1_overlap" not in training_args.sharding_parallel_config
#             ), "Currently not support enabling sharding_stage1_overlap in lora mode."
#         if model_args.lora_path is None:
#             target_modules = get_lora_target_modules(model)
#             lora_config = LoRAConfig(
#                 target_modules=target_modules,
#                 r=model_args.lora_rank,
#                 lora_alpha=2 * model_args.lora_rank if not model_args.rslora else 4,
#                 rslora=model_args.rslora,
#                 lora_plus_scale=model_args.lora_plus_scale,
#                 pissa=model_args.pissa,
#                 merge_weights=False,
#                 tensor_parallel_degree=training_args.tensor_parallel_degree,
#                 dtype=dtype,
#                 base_model_name_or_path=model_args.model_name_or_path,
#                 use_quick_lora=model_args.use_quick_lora,
#                 lora_use_mixer=model_args.lora_use_mixer,
#             )
#             model = LoRAModel(model, lora_config)
#         else:
#             model = LoRAModel.from_pretrained(model=model, lora_path=model_args.lora_path)

#         model.print_trainable_parameters()

#     if model_args.lokr:
#         if model_args.lokr_path is None:
#             target_modules = get_lora_target_modules(model)
#             lokr_config = LoKrConfig(
#                 target_modules=target_modules,
#                 lokr_dim=model_args.lokr_dim,
#                 dtype=dtype,
#                 base_model_name_or_path=model_args.model_name_or_path,
#             )
#             model = LoKrModel(model, lokr_config)
#         else:
#             model = LoKrModel.from_pretrained(model=model, lokr_path=model_args.lokr_path)

#     if model_args.reft:
#         intervention_dtype = dtype
#         intervention_params = {
#             "embed_dim": model_config.hidden_size,
#             "low_rank_dimension": reft_args.rank,
#             "dropout": reft_args.dropout,
#             "dtype": intervention_dtype,
#             "act_fn": reft_args.act_fn,
#             "device": "gpu",
#             "add_bias": reft_args.add_bias,
#         }
#         representations = [
#             {
#                 "layer": l,
#                 "component": "block_output",
#                 "low_rank_dimension": reft_args.rank,
#                 "intervention": intervention_mapping[reft_args.intervention_type](**intervention_params),
#             }
#             for l in reft_layers
#         ]
#         reft_config = ReFTConfig(
#             representations=representations, intervention_params=intervention_params, position=reft_args.position
#         )
#         # get reft model
#         model = ReFTModel(reft_config, model)
#         # disable origianl model gradients
#         model.disable_model_gradients()
#         model.print_trainable_parameters()

#     if model_args.vera:
#         target_modules = get_lora_target_modules(model)
#         vera_config = VeRAConfig(
#             target_modules=target_modules,
#             r=model_args.vera_rank,
#             vera_alpha=model_args.vera_rank,
#             dtype=dtype,
#             base_model_name_or_path=model_args.model_name_or_path,
#             pissa_init=True,
#         )
#         model = VeRAModel(model, vera_config)
#         model.mark_only_vera_as_trainable(notfreezeB=True)
#         model.print_trainable_parameters()

#     return model



# class PeftModel(PushToHubMixin, paddle.nn.Module):
#     """
#     Base model encompassing various Peft methods.

#     Args:
#         model ([`~transformers.PreTrainedModel`]): The base transformer model used for Peft.
#         peft_config ([`PeftConfig`]): The configuration of the Peft model.
#         adapter_name (`str`,  *optional*): The name of the adapter, defaults to `"default"`.
#         autocast_adapter_dtype (`bool`, *optional*):
#             Whether to autocast the adapter dtype. Defaults to `True`. Right now, this will only cast adapter weights
#             using float16 and bfloat16 to float32, as this is typically required for stable training, and only affect
#             select PEFT tuners.
#         low_cpu_mem_usage (`bool`, `optional`, defaults to `False`):
#             Create empty adapter weights on meta device. Useful to speed up the loading loading process.

#             <Tip>

#             Don't use `low_cpu_mem_usage=True` when creating a new PEFT adapter for training.

#             </Tip>

#     **Attributes**:
#         - **base_model** ([`paddle.nn.Layer`]) -- The base transformer model used for Peft.
#         - **peft_config** ([`PeftConfig`]) -- The configuration of the Peft model.
#         - **modules_to_save** (`list` of `str`) -- The list of sub-module names to save when
#             saving the model.
#         - **prompt_encoder** ([`PromptEncoder`]) -- The prompt encoder used for Peft if
#             using [`PromptLearningConfig`].
#         - **prompt_tokens** (`paddle.Tensor`) -- The virtual prompt tokens used for Peft if
#             using [`PromptLearningConfig`].
#         - **transformer_backbone_name** (`str`) -- The name of the transformer
#             backbone in the base model if using [`PromptLearningConfig`].
#         - **word_embeddings** (`paddle.nn.Embedding`) -- The word embeddings of the transformer backbone
#             in the base model if using [`PromptLearningConfig`].
#     """

#     def __init__(
#         self,
#         model: PreTrainedModel,
#         peft_config: PeftConfig,
#         adapter_name: str = "default",
#         autocast_adapter_dtype: bool = True,
#         low_cpu_mem_usage: bool = False,
#     ) -> None:
#         super().__init__()
#         self.modules_to_save = None
#         self.active_adapter = adapter_name
#         self.peft_type = peft_config.peft_type
#         # These args are special PEFT arguments that users can pass. They need to be removed before passing them to
#         # forward.
#         self.special_peft_forward_args = {"adapter_names"}

#         self._is_prompt_learning = peft_config.is_prompt_learning
#         if self._is_prompt_learning:
#             self._peft_config = {adapter_name: peft_config}
#             self.base_model = model
#             self.add_adapter(adapter_name, peft_config, low_cpu_mem_usage=low_cpu_mem_usage)
#         else:
#             self._peft_config = None
#             cls = PEFT_TYPE_TO_MODEL_MAPPING[peft_config.peft_type]
#             ctx = init_empty_weights if low_cpu_mem_usage else nullcontext
#             with ctx():
#                 self.base_model = cls(model, {adapter_name: peft_config}, adapter_name)
#             self.set_additional_trainable_modules(peft_config, adapter_name)

#         if hasattr(self.base_model, "_cast_adapter_dtype"):
#             self.base_model._cast_adapter_dtype(
#                 adapter_name=adapter_name, autocast_adapter_dtype=autocast_adapter_dtype
#             )

#         if getattr(model, "is_gradient_checkpointing", True):
#             model = self._prepare_model_for_gradient_checkpointing(model)

#         # the `pretraining_tp` is set for some models to simulate Tensor Parallelism during inference to avoid
#         # numerical differences, https://github.com/pytorch/pytorch/issues/76232 - to avoid any unexpected
#         # behavior we disable that in this line.
#         if hasattr(self.base_model, "config") and hasattr(self.base_model.config, "pretraining_tp"):
#             self.base_model.config.pretraining_tp = 1

#     @property
#     def peft_config(self) -> dict[str, PeftConfig]:
#         if self._is_prompt_learning:
#             return self._peft_config
#         return self.base_model.peft_config

#     @property
#     def active_adapters(self) -> list[str]:
#         try:
#             adapters = self.base_model.active_adapters
#             if not isinstance(adapters, list):
#                 # Base model is probably a transformers model, see:
#                 # https://github.com/huggingface/transformers/pull/30790#issuecomment-2253808249
#                 # Unfortunately, transformers models also have an active_adapters method but it's 1) not a property and
#                 # 2) calling it fails because the base model (usually) has no loaded adapter. The base model can be a
#                 # transformers model for prompt learning, where the base model is not wrapped in a LoraModel or similar.
#                 adapters = self.active_adapter
#                 if isinstance(adapters, str):
#                     adapters = [adapters]
#         except AttributeError:
#             adapters = self.active_adapter
#             if isinstance(adapters, str):
#                 adapters = [adapters]
#         return adapters

#     @peft_config.setter
#     def peft_config(self, value: dict[str, PeftConfig]):
#         if self._is_prompt_learning:
#             self._peft_config = value
#         else:
#             self.base_model.peft_config = value

#     def save_pretrained(
#         self,
#         save_directory: str,
#         safe_serialization: bool = True,
#         selected_adapters: Optional[list[str]] = None,
#         save_embedding_layers: Union[str, bool] = "auto",
#         is_main_process: bool = True,
#         path_initial_model_for_weight_conversion: Optional[str] = None,
#         **kwargs: Any,
#     ) -> None:
#         r"""
#         This function saves the adapter model and the adapter configuration files to a directory, so that it can be
#         reloaded using the [`PeftModel.from_pretrained`] class method, and also used by the [`PeftModel.push_to_hub`]
#         method.

#         Args:
#             save_directory (`str`):
#                 Directory where the adapter model and configuration files will be saved (will be created if it does not
#                 exist).
#             safe_serialization (`bool`, *optional*):
#                 Whether to save the adapter files in safetensors format, defaults to `True`.
#             selected_adapters (`List[str]`,  *optional*):
#                 A list of adapters to be saved. If `None`, will default to all adapters.
#             save_embedding_layers (`Union[bool, str]`, *optional*, defaults to `"auto"`):
#                 If `True`, save the embedding layers in addition to adapter weights. If `auto`, checks the common
#                 embedding layers `peft.utils.other.EMBEDDING_LAYER_NAMES` in config's `target_modules` when available.
#                 and automatically sets the boolean flag. This only works for 🤗 transformers models.
#             is_main_process (`bool`, *optional*):
#                 Whether the process calling this is the main process or not. Will default to `True`. Will not save the
#                 checkpoint if not on the main process, which is important for multi device setups (e.g. DDP).
#             path_initial_model_for_weight_conversion (`str, *optional*`):
#                 The path to the initialized adapter, which is obtained after initializing the model with PiSSA or OLoRA
#                 and before performing any training. When `path_initial_model_for_weight_conversion` is not None, the
#                 difference in adapter before and after fine-tuning is calculated. This difference can be represented as
#                 the parameters of a standard LoRA adapter. Using this converted adapter does not require changes to the
#                 base model, thus conveniently allowing the use of multiple PiSSA or OLoRA adapters with LoRA adapters,
#                 and the activation or deactivation of any adapters. Note that this conversion is not supported if
#                 `rslora` is used in combination with `rank_pattern` or `alpha_pattern`.
#             kwargs (additional keyword arguments, *optional*):
#                 Additional keyword arguments passed along to the `push_to_hub` method.

#         """
#         if os.path.isfile(save_directory):
#             raise ValueError(f"Provided path ({save_directory}) should be a directory, not a file")

#         if selected_adapters is None:
#             selected_adapters = list(self.peft_config.keys())
#         else:
#             if any(
#                 selected_adapter_name not in list(self.peft_config.keys())
#                 for selected_adapter_name in selected_adapters
#             ):
#                 raise ValueError(
#                     f"You passed an invalid `selected_adapters` arguments, current supported adapter names are"
#                     f" {list(self.peft_config.keys())} - got {selected_adapters}."
#                 )

#         def save_mutated_as_lora(peft_config, path_initial_model_for_weight_conversion, output_state_dict, kwargs):
#             if peft_config.use_rslora and (peft_config.rank_pattern or peft_config.alpha_pattern):
#                 msg = (
#                     "Passing `path_initial_model_for_weight_conversion` to `save_pretrained` is not supported when "
#                     "using `rank_pattern` or `alpha_pattern` at the same time as `use_rslora=True`."
#                 )
#                 raise ValueError(msg)

#             if not any(
#                 str(peft_config.init_lora_weights).lower().startswith(prefix) for prefix in ["pissa", "olora", "true"]
#             ):
#                 warnings.warn(
#                     "`path_initial_model_for_weight_conversion` only works for converting a PiSSA or OLoRA adapter to "
#                     "a LoRA adapter"
#                 )
#             initial_adapter_name = os.path.basename(path_initial_model_for_weight_conversion)
#             try:
#                 self.load_adapter(
#                     os.path.dirname(path_initial_model_for_weight_conversion),
#                     subfolder=initial_adapter_name,
#                     adapter_name=initial_adapter_name,
#                 )
#                 is_pissa = str(self.peft_config[initial_adapter_name].init_lora_weights).lower().startswith("pissa")
#                 is_olora = str(self.peft_config[initial_adapter_name].init_lora_weights).lower() == "olora"
#                 if is_pissa or is_olora:
#                     raise ValueError(
#                         "The `init_lora_weights` parameter of the initial adapter should be set to `True`. "
#                         "Otherwise, `self.load_adapter` will subtract the decomposed values again based on the "
#                         "residual model."
#                     )
#                 output_state_dict = self.base_model.subtract_mutated_init(
#                     output_state_dict, initial_adapter_name, kwargs
#                 )
#             finally:
#                 self.delete_adapter(initial_adapter_name)
#             return output_state_dict

#         if is_main_process:
#             os.makedirs(save_directory, exist_ok=True)
#             self.create_or_update_model_card(save_directory)

#         for adapter_name in selected_adapters:
#             peft_config = self.peft_config[adapter_name]
#             # save only the trainable weights
#             output_state_dict = get_peft_model_state_dict(
#                 self,
#                 state_dict=kwargs.get("state_dict", None),
#                 adapter_name=adapter_name,
#                 save_embedding_layers=save_embedding_layers,
#             )
#             output_dir = os.path.join(save_directory, adapter_name) if adapter_name != "default" else save_directory
#             os.makedirs(output_dir, exist_ok=True)

#             if is_main_process and safe_serialization:
#                 # Section copied from: https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_utils.py#L2111-L2134
#                 # Safetensors does not allow tensor aliasing.
#                 # We're going to remove aliases before saving
#                 ptrs = collections.defaultdict(list)
#                 for name, tensor in output_state_dict.items():
#                     # Sometimes in the state_dict we have non-tensor objects.
#                     # e.g. in bitsandbytes we have some `str` objects in the state_dict
#                     if isinstance(tensor, paddle.Tensor):
#                         ptrs[id_tensor_storage(tensor)].append(name)
#                     else:
#                         # In the non-tensor case, fall back to the pointer of the object itself
#                         ptrs[id(tensor)].append(name)

#                 # These are all the pointers of shared tensors.
#                 shared_ptrs = {ptr: names for ptr, names in ptrs.items() if len(names) > 1}

#                 for _, names in shared_ptrs.items():
#                     # Here we just clone the shared tensors to avoid tensor aliasing which is
#                     # not supported in safetensors.
#                     for shared_tensor_name in names[1:]:
#                         output_state_dict[shared_tensor_name] = output_state_dict[shared_tensor_name].clone()
#                 if path_initial_model_for_weight_conversion is not None:
#                     peft_config = copy.deepcopy(peft_config)
#                     peft_config.init_lora_weights = True
#                     peft_config.save_pretrained(path_initial_model_for_weight_conversion)
#                     output_state_dict = save_mutated_as_lora(
#                         peft_config, path_initial_model_for_weight_conversion, output_state_dict, kwargs
#                     )
#                 safe_save_file(
#                     output_state_dict,
#                     os.path.join(output_dir, SAFETENSORS_WEIGHTS_NAME),
#                     metadata={"format": "pt"},
#                 )
#             elif is_main_process:
#                 if path_initial_model_for_weight_conversion is not None:
#                     peft_config = copy.deepcopy(peft_config)
#                     peft_config.init_lora_weights = True
#                     peft_config.save_pretrained(path_initial_model_for_weight_conversion)
#                     output_state_dict = save_mutated_as_lora(
#                         peft_config, path_initial_model_for_weight_conversion, output_state_dict, kwargs
#                     )
#                 paddle.save(output_state_dict, os.path.join(output_dir, WEIGHTS_NAME))

#             # save the config and change the inference mode to `True`
#             if peft_config.base_model_name_or_path is None:
#                 peft_config.base_model_name_or_path = (
#                     self.base_model.__dict__.get("name_or_path", None)
#                     if peft_config.is_prompt_learning
#                     else self.base_model.model.__dict__.get("name_or_path", None)
#                 )
#             inference_mode = peft_config.inference_mode
#             peft_config.inference_mode = True

#             if peft_config.task_type is None:
#                 # deal with auto mapping
#                 base_model_class = self._get_base_model_class(
#                     is_prompt_tuning=peft_config.is_prompt_learning,
#                 )
#                 parent_library = base_model_class.__module__

#                 auto_mapping_dict = {
#                     "base_model_class": base_model_class.__name__,
#                     "parent_library": parent_library,
#                 }
#             else:
#                 auto_mapping_dict = None

#             if is_main_process:
#                 if path_initial_model_for_weight_conversion is not None:
#                     peft_config.init_lora_weights = True
#                     peft_config.r *= 2
#                     if not peft_config.use_rslora:
#                         peft_config.lora_alpha *= 2
#                     else:
#                         # with rslora, we have scaling = alpha / sqrt(r), we thus adjust alpha to keep the same scaling
#                         peft_config.lora_alpha *= 2**0.5

#                     if peft_config.rank_pattern:
#                         peft_config.rank_pattern = {key: 2 * val for key, val in peft_config.rank_pattern.items()}
#                     if peft_config.alpha_pattern:
#                         peft_config.alpha_pattern = {key: 2 * val for key, val in peft_config.alpha_pattern.items()}

#                 peft_config.save_pretrained(output_dir, auto_mapping_dict=auto_mapping_dict)
#             peft_config.inference_mode = inference_mode

#     @classmethod
#     def from_pretrained(
#         cls,
#         model: paddle.nn.Layer,
#         model_id: Union[str, os.PathLike],
#         adapter_name: str = "default",
#         is_trainable: bool = False,
#         config: Optional[PeftConfig] = None,
#         autocast_adapter_dtype: bool = True,
#         ephemeral_gpu_offload: bool = False,
#         low_cpu_mem_usage: bool = False,
#         **kwargs: Any,
#     ) -> PeftModel:
#         r"""
#         Instantiate a PEFT model from a pretrained model and loaded PEFT weights.

#         Note that the passed `model` may be modified inplace.

#         Args:
#             model ([`paddle.nn.Layer`]):
#                 The model to be adapted. For 🤗 Transformers models, the model should be initialized with the
#                 [`~transformers.PreTrainedModel.from_pretrained`].
#             model_id (`str` or `os.PathLike`):
#                 The name of the PEFT configuration to use. Can be either:
#                     - A string, the `model id` of a PEFT configuration hosted inside a model repo on the Hugging Face
#                       Hub.
#                     - A path to a directory containing a PEFT configuration file saved using the `save_pretrained`
#                       method (`./my_peft_config_directory/`).
#             adapter_name (`str`, *optional*, defaults to `"default"`):
#                 The name of the adapter to be loaded. This is useful for loading multiple adapters.
#             is_trainable (`bool`, *optional*, defaults to `False`):
#                 Whether the adapter should be trainable or not. If `False`, the adapter will be frozen and can only be
#                 used for inference.
#             config ([`~peft.PeftConfig`], *optional*):
#                 The configuration object to use instead of an automatically loaded configuration. This configuration
#                 object is mutually exclusive with `model_id` and `kwargs`. This is useful when configuration is already
#                 loaded before calling `from_pretrained`.
#             autocast_adapter_dtype (`bool`, *optional*):
#                 Whether to autocast the adapter dtype. Defaults to `True`. Only relevant for specific adapter types.
#             ephemeral_gpu_offload (`bool`, *optional*):
#                 Whether to use ephemeral GPU offloading for partially loaded modules. Defaults to `False`. This is
#                 useful when parts of the model and/or components (such as adapters) are kept in CPU memory until they
#                 are needed. Rather than perform expensive operations on small data, the data is transferred to the GPU
#                 on-demand, the operation(s) performed, and the results moved back to CPU memory. This brings a slight
#                 momentary VRAM overhead but gives orders of magnitude speedup in certain cases.
#             low_cpu_mem_usage (`bool`, `optional`, defaults to `False`):
#                 Create empty adapter weights on meta device before loading the saved weights. Useful to speed up the
#                 process.
#             paddle_device (`str`, *optional*, defaults to None):
#                 The device to load the adapter on. If `None`, the device will be inferred.
#             kwargs: (`optional`):
#                 Additional keyword arguments passed along to the specific PEFT configuration class.
#         """
#         from .mapping import MODEL_TYPE_TO_PEFT_MODEL_MAPPING, PEFT_TYPE_TO_CONFIG_MAPPING

#         # load the config
#         if config is None:
#             config = PEFT_TYPE_TO_CONFIG_MAPPING[
#                 PeftConfig._get_peft_type(
#                     model_id,
#                     subfolder=kwargs.get("subfolder", None),
#                     revision=kwargs.get("revision", None),
#                     cache_dir=kwargs.get("cache_dir", None),
#                     use_auth_token=kwargs.get("use_auth_token", None),
#                     token=kwargs.get("token", None),
#                 )
#             ].from_pretrained(model_id, **kwargs)
#         elif isinstance(config, PeftConfig):
#             config.inference_mode = not is_trainable
#         else:
#             raise ValueError(f"The input config must be a PeftConfig, got {config.__class__}")

#         # Runtime configuration, if supported
#         if hasattr(config, "runtime_config"):
#             config.runtime_config.ephemeral_gpu_offload = ephemeral_gpu_offload
#         else:
#             if ephemeral_gpu_offload:
#                 warnings.warn("Ephemeral GPU offloading is not supported for this model. Ignoring.")

#         if hasattr(model, "hf_device_map"):
#             weight_map = dict(named_module_tensors(model, recurse=True))

#             # recreate the offload_index for disk-offloaded modules: we need to know the location in storage of each weight
#             # before the offload hook is removed from the model
#             disk_modules = set()
#             index = None
#             for name, module in model.named_modules():
#                 if hasattr(module, "_hf_hook") and hasattr(module._hf_hook, "original_devices"):
#                     if hasattr(module._hf_hook.weights_map, "dataset"):
#                         index = module._hf_hook.weights_map.dataset.index
#                     for key in module._hf_hook.original_devices.keys():
#                         if module._hf_hook.original_devices[key] == paddle.device("meta"):
#                             disk_modules.add(str(name) + "." + str(key))

#             if disk_modules and not kwargs.get("use_safetensors", True):
#                 raise ValueError("Disk offloading currently only supported for safetensors")

#             if index:
#                 offload_index = {
#                     p: {
#                         "safetensors_file": index[p]["safetensors_file"],
#                         "weight_name": p,
#                         "dtype": str(weight_map[p].dtype).replace("paddle.", ""),
#                     }
#                     for p in weight_map.keys()
#                     if p in disk_modules
#                 }
#                 kwargs["offload_index"] = offload_index

#         if (getattr(model, "hf_device_map", None) is not None) and len(
#             set(model.hf_device_map.values()).intersection({"cpu", "disk"})
#         ) > 0:
#             remove_hook_from_submodules(model)

#         if config.is_prompt_learning and is_trainable:
#             raise ValueError("Cannot set a prompt learning adapter to trainable when loading pretrained adapter.")
#         else:
#             config.inference_mode = not is_trainable
#         if isinstance(getattr(model, "base_model", None), XLoraModel):
#             if not isinstance(config, XLoraConfig):
#                 raise TypeError(f"Expected 'XLoraConfig', got '{type(config)}' instead.")
#             if "adapters" in kwargs:
#                 config.adapters = kwargs["adapters"]
#             else:
#                 # If the path is on HF hub, then we get the adapter names to create a subfolders list which tells
#                 # `load_adapter` where the adapters are.
#                 if not os.path.exists(model_id):
#                     s = HfFileSystem()

#                     # The names of the adapters which must be in folders
#                     adapter_names = [
#                         file["name"][len(model_id) + 1 :] for file in s.ls(model_id) if file["type"] == "directory"
#                     ]
#                     # Prepare a dict of adapter paths, which really just point to the hf id; we will use the subfolders
#                     adapter_paths = {}
#                     for adapter_name in adapter_names:
#                         adapter_paths[adapter_name] = os.path.join(model_id, model_id)
#                     config.adapters = adapter_paths
#                     config._subfolders = adapter_names
#                 else:
#                     if "adapters" not in kwargs:
#                         raise ValueError("If model_id is a local path, then `adapters` must be passed in kwargs.")

#         if config.task_type not in MODEL_TYPE_TO_PEFT_MODEL_MAPPING.keys():
#             model = cls(
#                 model,
#                 config,
#                 adapter_name,
#                 autocast_adapter_dtype=autocast_adapter_dtype,
#                 low_cpu_mem_usage=low_cpu_mem_usage,
#             )
#         else:
#             model = MODEL_TYPE_TO_PEFT_MODEL_MAPPING[config.task_type](
#                 model,
#                 config,
#                 adapter_name,
#                 autocast_adapter_dtype=autocast_adapter_dtype,
#                 low_cpu_mem_usage=low_cpu_mem_usage,
#             )

#         load_result = model.load_adapter(
#             model_id,
#             adapter_name,
#             is_trainable=is_trainable,
#             autocast_adapter_dtype=autocast_adapter_dtype,
#             low_cpu_mem_usage=low_cpu_mem_usage,
#             **kwargs,
#         )

#         # 1. Remove VB-LoRA vector bank, since it's a shared parameter set via the VBLoRAModel
#         # 2. Remove the prompt encoder, as it does not need to be part of the checkpoint
#         missing_keys = [
#             k for k in load_result.missing_keys if "vblora_vector_bank" not in k and "prompt_encoder" not in k
#         ]
#         if missing_keys:
#             # Let's warn here since (in contrast to load_adapter) we don't return the load result, so it could be quite
#             # difficult for users to even notice that something might have gone wrong here. As we filter out non PEFT
#             # keys from the missing keys, this gives no false positives.
#             warnings.warn(f"Found missing adapter keys while loading the checkpoint: {missing_keys}")

#         return model

#     def _setup_prompt_encoder(self, adapter_name: str):
#         config = self.peft_config[adapter_name]
#         if not hasattr(self, "prompt_encoder"):
#             self.prompt_encoder = paddle.nn.LayerDict({})
#             self.prompt_tokens = {}
#         transformer_backbone = None
#         for name, module in self.base_model.named_children():
#             for param in module.parameters():
#                 param.requires_grad = False
#             if isinstance(module, PreTrainedModel):
#                 # Make sure to freeze Tranformers model
#                 if transformer_backbone is None:
#                     transformer_backbone = module
#                     self.transformer_backbone_name = name
#         if transformer_backbone is None:
#             transformer_backbone = self.base_model

#         if config.num_transformer_submodules is None:
#             config.num_transformer_submodules = 2 if config.task_type == TaskType.SEQ_2_SEQ_LM else 1

#         # determine the word embeddings
#         word_embeddings = None
#         try:
#             # First try to find the word embeddings based on the module name, this should work for models like Bert,
#             # Roberta, Deberta, etc.
#             word_embeddings = self.base_model.get_submodule("embeddings.word_embeddings")
#         except AttributeError:
#             pass

#         if word_embeddings is None:
#             # Word embeddings could not be determined. Next try to guess them by checking which parameter has the size
#             # of the vocab.
#             for named_param, value in list(transformer_backbone.named_parameters()):
#                 # for ZeRO-3, the tensor is sharded across accelerators and deepspeed modifies it to a tensor with shape
#                 # [0] the actual unsharded shape is stored in "ds_shape" attribute special handling is needed in case
#                 # the model is initialized in deepspeed.zero.Init() context or HfDeepSpeedConfig has been called before
#                 # For reference refer to issue: https://github.com/huggingface/peft/issues/996
#                 deepspeed_distributed_tensor_shape = getattr(value, "ds_shape", None)

#                 if value.shape[0] == self.base_model.config.vocab_size or (
#                     deepspeed_distributed_tensor_shape is not None
#                     and deepspeed_distributed_tensor_shape[0] == self.base_model.config.vocab_size
#                 ):
#                     word_embeddings = transformer_backbone.get_submodule(named_param.replace(".weight", ""))
#                     break

#         self.word_embeddings = word_embeddings

#         if config.peft_type == PeftType.PROMPT_TUNING:
#             prompt_encoder = PromptEmbedding(config, self.word_embeddings)
#         elif config.peft_type == PeftType.MULTITASK_PROMPT_TUNING:
#             prompt_encoder = MultitaskPromptEmbedding(config, self.word_embeddings)
#         elif config.peft_type == PeftType.P_TUNING:
#             prompt_encoder = PromptEncoder(config)
#         elif config.peft_type == PeftType.PREFIX_TUNING:
#             # prefix tuning now uses Cache but that won't work with gradient checkpointing
#             if any(getattr(module, "gradient_checkpointing", False) for module in self.get_base_model().modules()):
#                 raise ValueError("Prefix tuning does not work with gradient checkpointing.")
#             prompt_encoder = PrefixEncoder(config)
#         elif config.peft_type == PeftType.CPT:
#             prompt_encoder = CPTEmbedding(config, self.word_embeddings)
#         else:
#             raise ValueError("Not supported")

#         prompt_encoder = prompt_encoder.to(self.device)
#         self.prompt_encoder.update(paddle.nn.LayerDict({adapter_name: prompt_encoder}))
#         self.prompt_tokens[adapter_name] = paddle.arange(
#             config.num_virtual_tokens * config.num_transformer_submodules
#         ).long()

#     def _prepare_model_for_gradient_checkpointing(self, model: PreTrainedModel):
#         r"""
#         Prepares the model for gradient checkpointing if necessary
#         """
#         if not (
#             getattr(model, "is_loaded_in_8bit", False)
#             or getattr(model, "is_loaded_in_4bit", False)
#             or getattr(model, "is_quantized", False)
#         ):
#             if hasattr(model, "enable_input_require_grads"):
#                 model.enable_input_require_grads()
#             elif hasattr(model, "get_input_embeddings"):

#                 def make_inputs_require_grad(module, input, output):
#                     output.requires_grad_(True)

#                 model.get_input_embeddings().register_forward_hook(make_inputs_require_grad)
#         return model

#     def get_prompt_embedding_to_save(self, adapter_name: str) -> paddle.Tensor:
#         """
#         Returns the prompt embedding to save when saving the model. Only applicable when using a prompt learning
#         method.
#         """
#         prompt_encoder = self.prompt_encoder[adapter_name]
#         prompt_tokens = (
#             self.prompt_tokens[adapter_name].unsqueeze(0).expand(1, -1).to(prompt_encoder.embedding.weight.device)
#         )
#         if self.peft_config[adapter_name].peft_type == PeftType.PREFIX_TUNING:
#             prompt_tokens = prompt_tokens[:, : self.peft_config[adapter_name].num_virtual_tokens]

#         if self.peft_config[adapter_name].peft_type == PeftType.MULTITASK_PROMPT_TUNING:
#             prompt_embeddings = super(MultitaskPromptEmbedding, prompt_encoder).forward(prompt_tokens)
#         else:
#             prompt_embeddings = prompt_encoder(prompt_tokens)

#         return prompt_embeddings[0].detach().cpu()

#     def get_prompt(self, batch_size: int, task_ids: Optional[paddle.Tensor] = None) -> paddle.Tensor:
#         """
#         Returns the virtual prompts to use for Peft. Only applicable when using a prompt learning method.
#         """
#         peft_config = self.active_peft_config
#         prompt_encoder = self.prompt_encoder[self.active_adapter]
#         prompt_tokens = (
#             self.prompt_tokens[self.active_adapter]
#             .unsqueeze(0)
#             .expand(batch_size, -1)
#             .to(prompt_encoder.embedding.weight.device)
#         )
#         if peft_config.peft_type == PeftType.PREFIX_TUNING:
#             prompt_tokens = prompt_tokens[:, : peft_config.num_virtual_tokens]
#             if peft_config.inference_mode:
#                 past_key_values = prompt_encoder.embedding.weight.repeat(batch_size, 1, 1)
#             else:
#                 past_key_values = prompt_encoder(prompt_tokens)
#             if self.base_model_paddle_dtype is not None:
#                 past_key_values = past_key_values.to(self.base_model_paddle_dtype)
#             past_key_values = past_key_values.view(
#                 batch_size,
#                 peft_config.num_virtual_tokens,
#                 peft_config.num_layers * 2,
#                 peft_config.num_attention_heads,
#                 peft_config.token_dim // peft_config.num_attention_heads,
#             )
#             if peft_config.num_transformer_submodules == 2:
#                 past_key_values = torch.cat([past_key_values, past_key_values], dim=2)
#             past_key_values = past_key_values.permute([2, 0, 3, 1, 4]).split(
#                 peft_config.num_transformer_submodules * 2
#             )
#             if TRANSFORMERS_MODELS_TO_PREFIX_TUNING_POSTPROCESS_MAPPING.get(self.config.model_type, None) is not None:
#                 post_process_fn = TRANSFORMERS_MODELS_TO_PREFIX_TUNING_POSTPROCESS_MAPPING[self.config.model_type]
#                 past_key_values = post_process_fn(past_key_values)
#             elif peft_config.num_transformer_submodules == 1:
#                 # Dont' apply this to encoder-decoder models and not to models requiring special processing.
#                 # local import in case users use a very old transformers version
#                 past_key_values = DynamicCache.from_legacy_cache(past_key_values)
#             elif peft_config.num_transformer_submodules == 2 and self.base_model._supports_cache_class:
#                 # Dont' apply this to encoder-decoder models that don't support new Cachc format yet
#                 # If we don't apply this, prefix-tuning fails to update cross-attn cache
#                 past_key_values = EncoderDecoderCache.from_legacy_cache(past_key_values)
#                 past_key_values.cross_attention_cache = DynamicCache()
#                 past_key_values.is_updated = {
#                     layer_idx: False for layer_idx in range(len(past_key_values.cross_attention_cache.key_cache))
#                 }
#             map_cache_to_layer_device_map(self.get_base_model(), past_key_values)  # no-op if not a Cache instance
#             return past_key_values
#         else:
#             if peft_config.peft_type == PeftType.MULTITASK_PROMPT_TUNING:
#                 prompts = prompt_encoder(prompt_tokens, task_ids)
#             else:
#                 if peft_config.inference_mode:
#                     prompts = prompt_encoder.embedding.weight
#                 else:
#                     # Take only one prompt token sample and expand the output instead of expanding the input, see:
#                     # https://github.com/huggingface/peft/issues/2043#issuecomment-2321522577
#                     prompt_tokens = prompt_tokens[:1]
#                     prompts = prompt_encoder(prompt_tokens)
#                 prompts = prompts.repeat(batch_size, 1, 1)
#             return prompts

#     def get_nb_trainable_parameters(self) -> tuple[int, int]:
#         r"""
#         Returns the number of trainable parameters and the number of all parameters in the model.
#         """
#         trainable_params = 0
#         all_param = 0
#         for _, param in self.named_parameters():
#             num_params = param.numel()
#             # if using DS Zero 3 and the weights are initialized empty
#             if num_params == 0 and hasattr(param, "ds_numel"):
#                 num_params = param.ds_numel

#             # Due to the design of 4bit linear layers from bitsandbytes
#             # one needs to multiply the number of parameters by 2 to get
#             # the correct number of parameters
#             if param.__class__.__name__ == "Params4bit":
#                 if hasattr(param, "element_size"):
#                     num_bytes = param.element_size()
#                 elif not hasattr(param, "quant_storage"):
#                     num_bytes = 1
#                 else:
#                     num_bytes = param.quant_storage.itemsize
#                 num_params = num_params * 2 * num_bytes

#             all_param += num_params
#             if param.requires_grad:
#                 trainable_params += num_params

#         return trainable_params, all_param

#     def print_trainable_parameters(self) -> None:
#         """
#         Prints the number of trainable parameters in the model.

#         Note: print_trainable_parameters() uses get_nb_trainable_parameters() which is different from
#         num_parameters(only_trainable=True) from huggingface/transformers. get_nb_trainable_parameters() returns
#         (trainable parameters, all parameters) of the Peft Model which includes modified backbone transformer model.
#         For techniques like LoRA, the backbone transformer model is modified in place with LoRA modules. However, for
#         prompt tuning, the backbone transformer model is unmodified. num_parameters(only_trainable=True) returns number
#         of trainable parameters of the backbone transformer model which can be different.
#         """
#         trainable_params, all_param = self.get_nb_trainable_parameters()

#         print(
#             f"trainable params: {trainable_params:,d} || all params: {all_param:,d} || trainable%: {100 * trainable_params / all_param:.4f}"
#         )

#     def __getattr__(self, name: str):
#         """Forward missing attributes to the wrapped module."""
#         try:
#             return super().__getattr__(name)  # defer to nn.Module's logic
#         except AttributeError:
#             if name == "base_model":  # see #1892: prevent infinite recursion if class is not initialized
#                 raise
#             return getattr(self.base_model, name)

#     @contextmanager
#     def _enable_peft_forward_hooks(self, *args, **kwargs):
#         # If the base model has a method called _enable_peft_forward_hooks, it is invoked as a context. Otherwise, this
#         # runs without any changes
#         if hasattr(self.base_model, "_enable_peft_forward_hooks"):
#             with self.base_model._enable_peft_forward_hooks(*args, **kwargs):
#                 yield
#             return
#         else:
#             # nothing to enable
#             yield
#             return

#     def forward(self, *args: Any, **kwargs: Any):
#         """
#         Forward pass of the model.
#         """
#         with self._enable_peft_forward_hooks(*args, **kwargs):
#             kwargs = {k: v for k, v in kwargs.items() if k not in self.special_peft_forward_args}
#             return self.get_base_model()(*args, **kwargs)

#     def generate(self, *args, **kwargs):
#         with self._enable_peft_forward_hooks(*args, **kwargs):
#             kwargs = {k: v for k, v in kwargs.items() if k not in self.special_peft_forward_args}
#             return self.get_base_model().generate(*args, **kwargs)

#     def _get_base_model_class(self, is_prompt_tuning=False):
#         """
#         Returns the base model class.
#         """
#         if not is_prompt_tuning:
#             return self.base_model.model.__class__
#         return self.base_model.__class__

#     @contextmanager
#     def disable_adapter(self):
#         """
#         Context manager that disables the adapter module. Use this to run inference on the base model.

#         Example:

#         ```py
#         >>> with model.disable_adapter():
#         ...     model(inputs)
#         ```
#         """
#         if self.peft_config[self.active_adapter].is_prompt_learning:
#             try:
#                 # TODO: consider replacing this patching of methods with a more robust mechanism: setting a flag and
#                 # letting the underlying methods deal with it, same as how LoRA does it.
#                 old_forward = self.forward
#                 self.forward = self.base_model.forward
#                 old_prepare_inputs_for_generation = self.prepare_inputs_for_generation
#                 self.prepare_inputs_for_generation = self.base_model.prepare_inputs_for_generation
#                 yield
#             finally:
#                 self.forward = old_forward
#                 self.prepare_inputs_for_generation = old_prepare_inputs_for_generation

#         elif self.peft_config[self.active_adapter].is_adaption_prompt:
#             try:
#                 self.base_model.disable_adapter_layers()
#                 yield
#             finally:
#                 self.base_model.enable_adapter_layers()

#         else:  # LoRA, LoHa, etc.
#             model_status = self.get_model_status()
#             if model_status.enabled == "irregular":
#                 warnings.warn(
#                     "The model contains some adapter layers that are enabled and others that are disabled. "
#                     "This is most likely unintentional. After exiting the disable_adapter context, all adapters "
#                     "will be enabled"
#                 )
#             try:
#                 self.base_model.disable_adapter_layers()
#                 yield
#             finally:
#                 if model_status.enabled is not False:
#                     # model_status.enabled is `True` or `"irregular"`
#                     self.base_model.enable_adapter_layers()

#     def get_base_model(self) -> paddle.nn.Layer:
#         """
#         Returns the base model.
#         """
#         return (
#             self.base_model
#             if (self.active_peft_config.is_prompt_learning or self.peft_type == PeftType.POLY)
#             else self.base_model.model
#         )

#     def add_adapter(self, adapter_name: str, peft_config: PeftConfig, low_cpu_mem_usage: bool = False) -> None:
#         """
#         Add an adapter to the model based on the passed configuration.

#         This adapter is not trained. To load a trained adapter, check out [`PeftModel.load_adapter`].

#         The name for the new adapter should be unique.

#         The new adapter is not automatically set as the active adapter. Use [`PeftModel.set_adapter`] to set the active
#         adapter.

#         Args:
#             adapter_name (`str`):
#                 The name of the adapter to be added.
#             peft_config ([`PeftConfig`]):
#                 The configuration of the adapter to be added.
#             low_cpu_mem_usage (`bool`, `optional`, defaults to `False`):
#                 Create empty adapter weights on meta device. Useful to speed up the process when loading saved
#                 adapters. Don't use this option when creating a new PEFT adapter for training.

#         """
#         if peft_config.peft_type != self.peft_type:
#             raise ValueError(
#                 f"Cannot combine adapters with different peft types. "
#                 f"Found {self.peft_type} and {peft_config.peft_type}."
#             )

#         try:
#             if peft_config.is_prompt_learning:
#                 self.peft_config[adapter_name] = peft_config
#                 if hasattr(self.config, "to_dict"):
#                     dict_config = self.config.to_dict()
#                 else:
#                     dict_config = self.config

#                 peft_config = _prepare_prompt_learning_config(peft_config, dict_config)
#                 self._setup_prompt_encoder(adapter_name)
#             elif peft_config.is_adaption_prompt:
#                 self.base_model.add_adapter(adapter_name, peft_config)
#             else:
#                 self.peft_config[adapter_name] = peft_config
#                 self.base_model.inject_adapter(
#                     self.base_model.model, adapter_name, low_cpu_mem_usage=low_cpu_mem_usage
#                 )
#         except Exception:  # something went wrong, roll back
#             if adapter_name in self.peft_config:
#                 del self.peft_config[adapter_name]
#             raise

#         self.set_additional_trainable_modules(peft_config, adapter_name)

#     def set_additional_trainable_modules(self, peft_config, adapter_name):
#         if getattr(peft_config, "modules_to_save", None) is not None:
#             if self.modules_to_save is None:
#                 self.modules_to_save = set(peft_config.modules_to_save)
#             else:
#                 self.modules_to_save.update(peft_config.modules_to_save)
#             _set_trainable(self, adapter_name)  # this may add a new ModulesToSaveWrapper

#     def get_layer_status(self) -> list[TunerLayerStatus]:
#         """Get the status of each adapter layer in the model.

#         This method returns a list of `TunerLayerStatus` dataclass instances, each of which contains the following
#         attributes:

#         - `name` (`str`):
#            The name of the adapter layer, e.g. `model.encoder.block.0.layer.0.SelfAttention.q`.
#         - `module_type` (`str`):
#            The type of the adapter layer, e.g. `lora.Linear`.
#         - `enabled` (`bool`):
#            Whether the adapter layer is enabled.
#         - `active_adapters` (`list[str]`):
#            The names of the active adapters, if any, e.g. `["default"]`.
#         - `merged_adapters` (`list[str]`):
#            The names of the merged adapters, if any, e.g. `["default"]`.
#         - `available_adapters` (`list[str]`):
#            The names of the available adapters, e.g. `["default"]`.

#         Args:
#             model ([`~PeftModel`]):
#                 The model to get the adapter layer status from.

#         Returns:
#             list[`peft.peft_model.TunerLayerStatus`]:
#                 A list of dataclasses, each containing the status of the corresponding adapter layer.

#         """
#         return get_layer_status(self)

#     def get_model_status(self) -> TunerModelStatus:
#         """Get the status of tuners of the model.

#         This method returns a `TunerModelStatus` dataclass instance, which contains the following attributes:

#         - `base_model_type` (`str`):
#            The type of the base model, e.g. `T5Model`.
#         - `adapter_model_type` (`str`):
#            The type of the adapter model, e.g. `LoraModel`.
#         - `peft_types` (`dict[str, str]`):
#            The mapping of adapter name to adapter type, e.g. `{"default": "LORA"}`.
#         - `trainable_params` (`int`):
#            The number of trainable parameters in the model.
#         - `total_params` (`int`):
#            The total number of parameters in the model.
#         - `num_adapter_layers` (`int`):
#            The number of adapter layers in the model.
#         - `enabled` (`bool`, `Literal["irregular"]`):
#            Whether all adapter layers are enabled. If some are enabled and some are not, this will be `"irregular"`.
#            This means that your model is in an inconsistent state and might not work as expected.
#         - `active_adapters` (`list[str]`, `Literal["irregular"]`):
#            The names of the active adapters. If the active adapters are not consistent across all layers, this will be
#            `"irregular"`, which means that your model is in an inconsistent state and might not work as expected.
#         - `merged_adapters` (`list[str]`, `Literal["irregular"]`):
#            The names of the merged adapters. If the merged adapters are not consistent across all layers, this will be
#            `"irregular"`, which means that your model is in an inconsistent state and might not work as expected.
#         - `available_adapters` (`list[str]`):
#            The names of the available adapters, e.g. `["default"]`.

#         Args:
#             model ([`~PeftModel`]):
#                 The model to get the adapter layer status from.

#         Returns:
#             `peft.peft_model.TunerModelStatus`:
#                 A dataclass containing the status of the model.

#         """
#         return get_model_status(self)

#     @classmethod
#     def _split_kwargs(cls, kwargs: dict[str, Any]):
#         _kwargs_not_in_hf_hub_download_signature = ("use_auth_token",)
#         hf_hub_download_kwargs = {}
#         other_kwargs = {}

#         for key, value in kwargs.items():
#             if key in inspect.signature(hf_hub_download).parameters or key in _kwargs_not_in_hf_hub_download_signature:
#                 hf_hub_download_kwargs[key] = value
#             else:
#                 other_kwargs[key] = value

#         return hf_hub_download_kwargs, other_kwargs

#     def _update_offload(self, offload_index: dict[str, dict[str, str]], adapters_weights: dict[str, paddle]):
#         """
#         Update the offload_index and safetensors files for loading and mergine PeftModels with disk-offloaded modules.

#         Args:
#             offload_index (Dict[str: str]):
#                 Dictionary of disk-offloaded modules with their metadata and safetensors filenames
#             adapters_weights (Dict[str: paddle.Tensor]):
#                 Dictionary of Peft adapter module names and weights
#         """

#         if not offload_index:
#             return offload_index

#         prefix = "base_model.model."
#         # rename offload index weight and model names
#         adapter_names = list(self.peft_config.keys())
#         for adapter_name in adapter_names:
#             keys = list(offload_index.keys())
#             block_id = keys[0].split(".")[0] + "."  # for writing safetensors key,

#             # replace original offload index keys with PeftModel keys
#             for key in keys:
#                 suffix_pos = key.rfind(".")
#                 extended_prefix = prefix + key[:suffix_pos]
#                 module = dict(self.named_modules())[extended_prefix]
#                 if isinstance(module, BaseTunerLayer):
#                     new_key = prefix + key[:suffix_pos] + ".base_layer" + key[suffix_pos:]
#                 else:
#                     new_key = prefix + key
#                 offload_index[key]["weight_name"] = new_key
#                 offload_index[new_key] = offload_index[key]
#                 del offload_index[key]

#             files_seen = set()
#             # rename safetensors for dispatch
#             for new_key in list(offload_index.keys()):
#                 fname = offload_index[new_key]["safetensors_file"]

#                 # make a new file name
#                 new_fname_list = list(fname.split(os.sep))
#                 for i, name in enumerate(new_fname_list):
#                     if "--" in name:
#                         new_fname_list[i] += "-peft"
#                         break
#                 new_fname = os.path.join(*new_fname_list)

#                 if fname in files_seen:
#                     continue
#                 safe_dict = {}
#                 with safe_open(fname, framework="pt") as f:
#                     for safe_key in f.keys():
#                         safe_tensor = f.get_tensor(safe_key)
#                         metadata = f.metadata()
#                         suffix_pos = safe_key.rfind(".")
#                         extended_prefix = prefix + block_id + safe_key[:suffix_pos]
#                         safe_module = dict(self.named_modules())[extended_prefix]
#                         if isinstance(safe_module, BaseTunerLayer):
#                             final_key = extended_prefix + ".base_layer" + safe_key[suffix_pos:]
#                             lora_dict = {key: val for key, val in adapters_weights.items() if extended_prefix in key}

#                             # add LoRA keys and values to disk offload
#                             for lora_key, lora_val in lora_dict.items():
#                                 divide = lora_key.rfind(".")
#                                 new_key = lora_key[:divide] + f".{adapter_name}" + lora_key[divide:]
#                                 safe_dict[new_key] = lora_val
#                         else:
#                             final_key = prefix + block_id + safe_key
#                         safe_dict[final_key] = safe_tensor
#                     files_seen.add(new_fname)

#                     # avoid overwriting original safetensors
#                     for key in safe_dict.keys():
#                         offload_index[key] = {"safetensors_file": new_fname, "weight_name": key}

#                     base_name = os.path.dirname(new_fname)
#                     if not os.path.exists(base_name):
#                         os.makedirs(base_name)
#                     safe_save_file(safe_dict, new_fname, metadata=metadata)

#     def _check_new_adapter_config(self, peft_config: PeftConfig, is_trainable: bool) -> None:
#         """Perform checks on newly added PEFT configs to ensure integrity."""
#         if peft_config.is_prompt_learning and is_trainable:
#             raise ValueError("Cannot set a prompt learning adapter to trainable when loading pretrained adapter.")

#         # Since PiSSA/OLoRA modifies the base weights, it should not be combined with other adapters.
#         all_configs = [peft_config] + list(self.peft_config.values())
#         if len(all_configs) > 1:
#             if any(getattr(config, "init_lora_weights", None) == "pissa" for config in all_configs):
#                 msg = (
#                     "PiSSA changes the base weights of the model and should thus not be used with other adapters. "
#                     "Consider converting the PiSSA adapter into a normal LoRA adapter: "
#                     "https://github.com/huggingface/peft/tree/main/examples/pissa_finetuning#convert-pissa-to-lora"
#                 )
#                 warnings.warn(msg)
#             elif any(getattr(config, "init_lora_weights", None) == "olora" for config in all_configs):
#                 msg = (
#                     "OLoRA changes the base weights of the model and should thus not be used with other adapters. "
#                     "Consider converting the OLoRA adapter into a normal LoRA adapter: "
#                     "https://github.com/huggingface/peft/tree/main/examples/olora_finetuning#olora-and-lora"
#                 )
#                 warnings.warn(msg)

#     def load_adapter(
#         self,
#         model_id: Union[str, os.PathLike],
#         adapter_name: str,
#         is_trainable: bool = False,
#         paddle_device: Optional[str] = None,
#         autocast_adapter_dtype: bool = True,
#         ephemeral_gpu_offload: bool = False,
#         low_cpu_mem_usage: bool = False,
#         **kwargs: Any,
#     ):
#         """
#         Load a trained adapter into the model.

#         The name for the new adapter should be unique.

#         The new adapter is not automatically set as the active adapter. Use [`PeftModel.set_adapter`] to set the active
#         adapter.

#         Args:
#             model_id (`str` or `os.PathLike`):
#                 The name of the PEFT configuration to use. Can be either:
#                     - A string, the `model id` of a PEFT configuration hosted inside a model repo on the Hugging Face
#                       Hub.
#                     - A path to a directory containing a PEFT configuration file saved using the `save_pretrained`
#                       method (`./my_peft_config_directory/`).
#             adapter_name (`str`):
#                 The name of the adapter to be added.
#             is_trainable (`bool`, *optional*, defaults to `False`):
#                 Whether the adapter should be trainable or not. If `False`, the adapter will be frozen and can only be
#                 used for inference.
#             paddle_device (`str`, *optional*, defaults to None):
#                 The device to load the adapter on. If `None`, the device will be inferred.
#             autocast_adapter_dtype (`bool`, *optional*, defaults to `True`):
#                 Whether to autocast the adapter dtype. Defaults to `True`. Right now, this will only cast adapter
#                 weights using float16 and bfloat16 to float32, as this is typically required for stable training, and
#                 only affect select PEFT tuners.
#             ephemeral_gpu_offload (`bool`, *optional*, defaults to `False`):
#                 Whether to use ephemeral GPU offloading for partially loaded modules. Defaults to `False`.
#             low_cpu_mem_usage (`bool`, `optional`, defaults to `False`):
#                 Create empty adapter weights on meta device before loading the saved weights. Useful to speed up the
#                 process.
#             kwargs: (`optional`):
#                 Additional arguments to modify the way the adapter is loaded, e.g. the token for Hugging Face Hub.
#         """
#         from .mapping import PEFT_TYPE_TO_CONFIG_MAPPING

#         hf_hub_download_kwargs, kwargs = self._split_kwargs(kwargs)
#         if paddle_device is None:
#             paddle_device = infer_device()

#         if adapter_name not in self.peft_config:
#             # load the config
#             peft_config = PEFT_TYPE_TO_CONFIG_MAPPING[
#                 PeftConfig._get_peft_type(
#                     model_id,
#                     **hf_hub_download_kwargs,
#                 )
#             ].from_pretrained(
#                 model_id,
#                 ephemeral_gpu_offload=ephemeral_gpu_offload,
#                 **hf_hub_download_kwargs,
#             )
#             self._check_new_adapter_config(peft_config, is_trainable=is_trainable)
#             peft_config.inference_mode = not is_trainable
#             self.add_adapter(adapter_name, peft_config, low_cpu_mem_usage=low_cpu_mem_usage)

#         adapters_weights = load_peft_weights(model_id, device=paddle_device, **hf_hub_download_kwargs)

#         # load the weights into the model
#         ignore_mismatched_sizes = kwargs.get("ignore_mismatched_sizes", False)
#         load_result = set_peft_model_state_dict(
#             self,
#             adapters_weights,
#             adapter_name=adapter_name,
#             ignore_mismatched_sizes=ignore_mismatched_sizes,
#             low_cpu_mem_usage=low_cpu_mem_usage,
#         )

#         tuner = self.peft_config[adapter_name].peft_type
#         tuner_prefix = PEFT_TYPE_TO_PREFIX_MAPPING.get(tuner, "")
#         adapter_missing_keys = []

#         # Filter missing keys specific to the current adapter and tuner prefix.
#         for key in load_result.missing_keys:
#             if tuner_prefix in key and adapter_name in key:
#                 adapter_missing_keys.append(key)

#         load_result.missing_keys.clear()
#         load_result.missing_keys.extend(adapter_missing_keys)

#         if (
#             (getattr(self, "hf_device_map", None) is not None)
#             and (len(set(self.hf_device_map.values()).intersection({"cpu", "disk"})) > 0)
#             and len(self.peft_config) == 1
#         ):
#             device_map = kwargs.get("device_map", "auto")
#             max_memory = kwargs.get("max_memory", None)
#             offload_dir = kwargs.get("offload_folder", None)
#             offload_index = kwargs.get("offload_index", None)

#             dispatch_model_kwargs = {}
#             # Safety checker for previous `accelerate` versions
#             # `offload_index` was introduced in https://github.com/huggingface/accelerate/pull/873/
#             if "offload_index" in inspect.signature(dispatch_model).parameters:
#                 dispatch_model_kwargs["offload_index"] = offload_index

#             no_split_module_classes = self._no_split_modules

#             if device_map != "sequential":
#                 max_memory = get_balanced_memory(
#                     self,
#                     max_memory=max_memory,
#                     no_split_module_classes=no_split_module_classes,
#                     low_zero=(device_map == "balanced_low_0"),
#                 )

#             if isinstance(device_map, str):
#                 device_map = infer_auto_device_map(
#                     self, max_memory=max_memory, no_split_module_classes=no_split_module_classes
#                 )

#             self._update_offload(offload_index, adapters_weights)
#             dispatch_model_kwargs["offload_index"] = offload_index

#             dispatch_model(
#                 self,
#                 device_map=device_map,
#                 offload_dir=offload_dir,
#                 **dispatch_model_kwargs,
#             )

#             hook = AlignDevicesHook(io_same_device=True)
#             if self.peft_config[adapter_name].is_prompt_learning:
#                 remove_hook_from_submodules(self.prompt_encoder)
#             add_hook_to_module(self.get_base_model(), hook)

#         if hasattr(self.base_model, "_cast_adapter_dtype"):
#             self.base_model._cast_adapter_dtype(
#                 adapter_name=adapter_name, autocast_adapter_dtype=autocast_adapter_dtype
#             )

#         # Set model in evaluation mode to deactivate Dropout modules by default
#         if not is_trainable:
#             self.eval()
#         return load_result

#     def set_adapter(self, adapter_name: str) -> None:
#         """
#         Sets the active adapter.

#         Only one adapter can be active at a time.

#         Additionally, this function will set the specified adapter to trainable (i.e., requires_grad=True). If this is
#         not desired, use the following code.

#         ```py
#         >>> for name, param in model_peft.named_parameters():
#         ...     if ...:  # some check on name (ex. if 'lora' in name)
#         ...         param.requires_grad = False
#         ```

#         Args:
#             adapter_name (`str`):
#                 The name of the adapter to be set as active. The adapter must be loaded first.
#         """
#         if adapter_name not in self.peft_config:
#             raise ValueError(f"Adapter {adapter_name} not found.")
#         self.active_adapter = adapter_name
#         if not self.peft_config[adapter_name].is_prompt_learning:
#             self.base_model.set_adapter(adapter_name)
#         _set_adapter(self, adapter_name)

#     @property
#     def base_model_paddle_dtype(self):
#         return getattr(self.base_model, "dtype", None)

#     @property
#     def active_peft_config(self):
#         return self.peft_config[self.active_adapter]

#     def create_or_update_model_card(self, output_dir: str):
#         """
#         Updates or create model card to include information about peft:
#         1. Adds `peft` library tag
#         2. Adds peft version
#         3. Adds base model info
#         4. Adds quantization information if it was used
#         """

#         filename = os.path.join(output_dir, "README.md")

#         card = ModelCard.load(filename) if os.path.exists(filename) else ModelCard.from_template(ModelCardData())

#         card.data["library_name"] = "peft"

#         model_config = BaseTuner.get_model_config(self)
#         model_config = None if model_config == DUMMY_MODEL_CONFIG else model_config
#         if model_config is not None and "_name_or_path" in model_config:
#             card.data["base_model"] = model_config["_name_or_path"]

#         lines = card.text.splitlines()

#         quantization_config = None
#         if hasattr(model_config, "quantization_config"):
#             quantization_config = self.config.quantization_config.to_dict()
#         training_config_text = ""
#         quantization_prefix = "The following `bitsandbytes` quantization config was used during training:"
#         # Adds quantization information if it was used
#         if quantization_config is not None:
#             training_config_text += f"\n{quantization_prefix}\n"
#             training_config_text += "\n".join([f"- {name}: {value}" for name, value in quantization_config.items()])
#             training_config_text += "\n"

#         training_procedure_heading = "## Training procedure"
#         if quantization_prefix not in lines and bool(training_config_text):
#             if training_procedure_heading in lines:
#                 lines.insert(lines.index(training_procedure_heading) + 2, training_config_text)
#             else:
#                 lines.append(f"{training_procedure_heading}\n{training_config_text}")

#         # Adds peft version
#         framework_block_heading = "### Framework versions"
#         if f"- PEFT {__version__}" not in lines:
#             if framework_block_heading in lines:
#                 lines.insert(lines.index(framework_block_heading) + 2, f"- PEFT {__version__}")
#             else:
#                 lines.append(f"{framework_block_heading}\n\n- PEFT {__version__}")

#         card.text = "\n".join(lines)
#         card.save(filename)

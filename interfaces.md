# Software System Interfaces（传统通用软件系统 Design Model）

> 语义 SSOT：[[cognition/software-system/README]]
> AIHW 边界：[[action/aihw/interfaces]]
> Host 消费：[[cognition/ai-workspace/07-semantic-model-host]]
> 分阶段落地：[[action/software-system/docs/plans]]

## Capability List

| Capability | Status | Description |
| --- | --- | --- |
| software_system.schema | v1 | System/Component/Module/Interface/DataModel/Runtime/Deployment/Dependency/ADR/ProjectionTarget 骨架对象定义（design_model.schema） |
| software_system.design_model | v1 | Design Model Provider 七操作实现（design_model.py：recognize / extract / validate / explain / propose_patch / project） |
| software_system.projection | v1 | ProjectionTarget 投影契约（design_model.project 产出 SoftwareSystemProjectionDraft/v1） |

## Design Model Skeleton（第一版）

| Object | Meaning |
| --- | --- |
| System | 系统边界、版本与顶层身份 |
| Component | 可部署 / 可替换的组成单元 |
| Module | 代码 / 逻辑模块 |
| Interface | 组件间契约（输入 / 输出 / 协议） |
| DataModel | 数据实体、关系与约束 |
| Runtime | 运行环境、进程与生命周期 |
| Deployment | 部署拓扑与环境映射 |
| Dependency | 依赖关系与版本约束 |
| ADR | 架构决策记录 |
| ProjectionTarget | 投影目标：architecture doc / docs / artifact 等 |

## ModelProvider 契约

- provider id：`software-system-design`
- model capability：`software_system.design_model_provider`
- 声明文件：`action/software-system/semantic-model.json`
 - 实现文件：`action/software-system/design_model.py`（七操作均为 v1 实现，draft-first）

| Operation | v1 状态 | 说明 |
| --- | --- | --- |
| schema | implemented | 返回 10 个骨架对象定义与边界 |
| recognize | implemented | 从 AIHW CanvasSnapshot / ContentSelection 识别软件系统模型实例（无组件时返回 exit 1） |
| extract | implemented | 抽取 SoftwareSystemView/v1（components + dependencies） |
| validate | implemented | 校验模型视图（重复 id / dangling dependency，结构化 issues） |
| explain | implemented | 解释组件、依赖、架构决策（markdown） |
| proposePatch | implemented | 生成 SoftwareSystemProposal/v1（draft-first） |
| project | implemented | 投影到 ProjectionTarget（SoftwareSystemProjectionDraft/v1） |

## 边界

- software-system 拥有传统软件系统 Design Model；不拥有 Agentic Software 范式（agentic-software），不承担 AIHW 语义宿主职责。
- 对 AIHW canvas 的任何写回必须走 AIHW ElementMutationProposal / approval。
- 禁止反模式（只允许出现在禁止规则段落中）：
  - "AIHW owns Software Design Model / AIHW owns Semantic Model"
  - "agentic-software = traditional software system（software-system = agentic-software）"
  - "Workflow 是唯一 Canvas Model（Canvas = Workflow）"

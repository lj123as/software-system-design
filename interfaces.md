# Software System Interfaces（传统通用软件系统 Design Model）

> 语义 SSOT：[[cognition/software-system/README]]
> AIHW 边界：[[action/aihw/interfaces]]
> Host 消费：[[cognition/ai-workspace/07-semantic-model-host]]
> 分阶段落地：[[action/software-system/docs/plans]]

## Capability List

| Capability | Status | Description |
| --- | --- | --- |
| software_system.schema | v1 skeleton | System/Component/Module/Interface/DataModel/Runtime/Deployment/Dependency/ADR/ProjectionTarget 骨架对象定义 |
| software_system.design_model | v1 skeleton | Design Model Provider 契约（ModelProvider 7 操作声明，recognize/extract/validate/explain/proposePatch/project 预留） |
| software_system.projection | reserved | ProjectionTarget 投影契约 |

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

| Operation | v1 状态 | 说明 |
| --- | --- | --- |
| schema | skeleton | 返回 10 个骨架对象定义与边界 |
| recognize | reserved | 从 AIHW CanvasSnapshot / ContentSelection 识别软件系统模型实例 |
| extract | reserved | 抽取 System/Component/Module/Interface 视图 |
| validate | reserved | 校验模型视图（结构化 issues） |
| explain | reserved | 解释组件、依赖、架构决策 |
| proposePatch | reserved | 生成模型补丁提案（draft-first） |
| project | reserved | 投影到 ProjectionTarget（architecture/doc/artifact） |

## 边界

- software-system 拥有传统软件系统 Design Model；不拥有 Agentic Software 范式（agentic-software），不承担 AIHW 语义宿主职责。
- 对 AIHW canvas 的任何写回必须走 AIHW ElementMutationProposal / approval。
- 禁止反模式（只允许出现在禁止规则段落中）：
  - "AIHW owns Software Design Model / AIHW owns Semantic Model"
  - "agentic-software = traditional software system（software-system = agentic-software）"
  - "Workflow 是唯一 Canvas Model（Canvas = Workflow）"

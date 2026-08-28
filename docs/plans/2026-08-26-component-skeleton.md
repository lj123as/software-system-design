# Software System 组件骨架落地计划

> 目标：新增 software-system_dev 组件（传统/通用软件系统 Design Model owner），与 agentic-software 区分并保持 AIHW 模型无关。

## 分阶段落地顺序

| 阶段 | 内容 | 状态 |
| --- | --- | --- |
| P0 cognition | cognition/software-system_dev/README.md：定位、与 agentic-software 对比、Skeleton Model 表 | 完成 |
| P1 action 骨架 | action/software-system_dev/component.yaml（software_system.schema / design_model / projection）+ interfaces.md（10 骨架对象 + ModelProvider 契约） | 完成 |
| P2 声明 | action/software-system_dev/semantic-model.json（provider id: software-system-design，7 操作 skeleton） | 完成 |
| P3 计划 | docs/plans 落地顺序与边界检查项 | 完成 |
| P4 实现 | design_model.py 七操作实现（schema/recognize/extract/validate/explain/propose_patch/project）+ tests/test_design_model.py；组件转为 git submodule（remote: lj123as/software-system） | 完成 |

## 边界检查项

- software-system 拥有传统软件系统 Design Model；不拥有 Agentic Software 范式。
- 不承担 AIHW 语义宿主职责；对 AIHW canvas 写回必须走 ElementMutationProposal / approval。
- 反模式（只允许出现在禁止段）："AIHW owns Software Design Model / AIHW owns Semantic Model"、"agentic-software = traditional software system"、"Workflow 是唯一 Canvas Model"。

## 验收标准

1. action/software-system_dev/component.yaml 存在且 provides 含 software_system.schema、software_system.design_model、software_system.projection。
2. action/software-system_dev/interfaces.md 明确 System / Component / Module / Interface / DataModel / Runtime / Deployment / Dependency / ADR / ProjectionTarget。
3. host discovery 能发现 software-system-design 且 owner_component == software-system。

## 执行状态

| 检查点 | 结果 |
| --- | --- |
| P0-P3 | 2026-08-26 完成 |
| 骨架断言 | test_semantic_model_host.py::test_software_system_component_skeleton_declares_traditional_design_model 通过 |
| P4 | 七操作 v1 实现 + 7 项单元测试通过；submodule 注册完成 |

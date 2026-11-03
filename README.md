# Microsoft Sentinel na prática — repositório do curso

Laboratórios, gabaritos e modelos do curso **Sentinel na prática** (Módulos 0, 2 e 4 — primeira versão).
Site do curso: https://bfrpaulondev.github.io/curso-sentinel/

O cenário é a **Loja Pixel**: uma loja online com API Node.js, usuários no Entra ID e pipeline no GitHub.
Na madrugada de 21/10/2026 ela sofre três ataques. Você acha cada um com KQL e escreve as regras que os detectam.

## Começar sem conta Azure (grátis)

```bash
docker run -d --name kusto -p 8080:8080 -e ACCEPT_EULA=Y mcr.microsoft.com/azuredataexplorer/kustainer-linux:latest
pip install azure-kusto-data pyyaml
python3 dataset/carregar_dataset.py        # cria o banco Loja e carrega o dataset fixo
./kql.py "SigninLogs | take 5"             # KQL de verdade, no emulador oficial
```

## Pastas

| Pasta | O que tem |
|---|---|
| `dataset/` | Gerador (seed fixa) e CSVs do dataset da Loja Pixel + script de carga |
| `api-loja/` | API Node.js da loja (sem dependências) que grava logs no formato `LojaApi_CL` |
| `labs/m0/` | Bicep do orçamento, workspace + Sentinel e App Service; script de deploy; setup local |
| `labs/m2/` | Consultas das aulas 2.1 a 2.6 |
| `labs/m4/` | Ataque de força bruta (só localhost), envio de logs, login suspeito sintético, regras YAML e o simulador local |
| `solucoes/` | Gabarito do teste do Módulo 2 |
| `grader/` | `corrigir.py` (teste do Módulo 2) e `testar_regra.py` (teste prático do Módulo 4) + CSVs esperados |
| `templates/` | Modelos de regra e de consulta |
| `respostas/` | Onde você coloca as suas respostas |

## Honestidade

- Todas as consultas foram executadas num Kusto real (Kustainer).
- O que precisa de subscrição (orçamento, workspace, Sentinel, App Service) está como código validado com `bicep lint`, mas não foi aplicado.
- `labs/m4/motor_regras_local.py` é um **simulador didático**. Ele **não é o Microsoft Sentinel**.
- Os logins do Entra ID são sintéticos.

## Testes

```bash
python3 grader/corrigir.py                  # Módulo 2: corrige respostas/m2/q01..q10.kql (mínimo 7/10)
python3 grader/testar_regra.py minha.yaml   # Módulo 4: ataca, roda a sua regra e exige um incidente
```

Antes do teste do Módulo 2, recarregue o dataset (`python3 dataset/carregar_dataset.py`), porque os labs do Módulo 4 inserem eventos novos.

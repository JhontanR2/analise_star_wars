import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Dados Manuais ---
data = [
    {"filme": "A New Hope", "ano": 1977, "orcamento": 11e6, "bilheteria": 775.398e6},
    {"filme": "The Empire Strikes Back", "ano": 1980, "orcamento": 18e6, "bilheteria": 550.016e6},
    {"filme": "Return of the Jedi", "ano": 1983, "orcamento": 32.5e6, "bilheteria": 482.466e6},
    {"filme": "The Phantom Menace", "ano": 1999, "orcamento": 115e6, "bilheteria": 1.0465e9},
    {"filme": "Attack of the Clones", "ano": 2002, "orcamento": 115e6, "bilheteria": 653.78e6},
    {"filme": "Revenge of the Sith", "ano": 2005, "orcamento": 113e6, "bilheteria": 905.596e6},
    {"filme": "The Force Awakens", "ano": 2015, "orcamento": 447e6, "bilheteria": 2.0713e9},
    {"filme": "The Last Jedi", "ano": 2017, "orcamento": 300e6, "bilheteria": 1.3344e9},
    {"filme": "The Rise of Skywalker", "ano": 2019, "orcamento": 416e6, "bilheteria": 1.0770e9},
    {"filme": "Rogue One", "ano": 2016, "orcamento": 232e6, "bilheteria": 1.0587e9},
    {"filme": "Solo: A Star Wars Story", "ano": 2018, "orcamento": 275e6, "bilheteria": 392.9248e6},
    {"filme": "The Clone Wars", "ano": 2008, "orcamento": 8.5e6, "bilheteria": 68.283e6},
]

df = pd.DataFrame(data)

# --- 2. Correção da inflação até 2025 ---
inflation = {
    1977: 5.1, 1980: 3.5, 1983: 3.2, 1999: 2.1, 2002: 2.3,
    2005: 3.4, 2008: 3.8, 2015: 0.1, 2016: 1.0, 2017: 2.1,
    2018: 2.4, 2019: 1.8, 2025: 2.5
}

def fator_acumulado(year):
    anos = [yr for yr in inflation if year <= yr <= 2025]
    fator = np.prod([(1 + inflation[yr] / 100) for yr in anos])
    return fator

df["fator_inflacao_ate_2025"] = df["ano"].apply(fator_acumulado)
df["orcamento_corrigido"] = df["orcamento"] * df["fator_inflacao_ate_2025"]
df["bilheteria_corrigida"] = df["bilheteria"] * df["fator_inflacao_ate_2025"]

# --- 3. Calcular lucro ---
df["lucro"] = df["bilheteria"] - df["orcamento"]
df["lucro_corrigido"] = df["bilheteria_corrigida"] - df["orcamento_corrigido"]

# --- 4. Ordenar cronicamente ---
df = df.sort_values("ano")

# --- 5. Gráficos ---
plt.style.use('seaborn-v0_8-whitegrid')

# Gráfico 1: Orçamento (Horizontal e Ordenado)
df_sorted_orcamento = df.sort_values("orcamento_corrigido", ascending=True)
fig1, ax1 = plt.subplots(figsize=(10, 7))
bars1 = ax1.barh(df_sorted_orcamento["filme"], df_sorted_orcamento["orcamento_corrigido"], color='#4A90E2')
ax1.set_title('Orçamento Corrigido por Filme (Valores de 2025)', fontsize=16, pad=20)
ax1.set_xlabel('Orçamento (em milhões de USD)', fontsize=12)
ax1.xaxis.set_major_formatter(lambda x, p: f'{x/1e6:.0f}M')
for bar in bars1:
    width = bar.get_width()
    ax1.text(width + 5e6, bar.get_y() + bar.get_height()/2, f'{width/1e6:.1f}M', ha='left', va='center', fontsize=9)
plt.tight_layout()


# Gráfico 2: Bilheteria (Horizontal e Ordenado)
df_sorted_bilheteria = df.sort_values("bilheteria_corrigida", ascending=True)
fig2, ax2 = plt.subplots(figsize=(10, 7))
bars2 = ax2.barh(df_sorted_bilheteria["filme"], df_sorted_bilheteria["bilheteria_corrigida"], color='#50E3C2')
ax2.set_title('Bilheteria Corrigida por Filme (Valores de 2025)', fontsize=16, pad=20)
ax2.set_xlabel('Bilheteria (em milhões de USD)', fontsize=12)
ax2.xaxis.set_major_formatter(lambda x, p: f'{x/1e6:.0f}M')
for bar in bars2:
    width = bar.get_width()
    ax2.text(width + 10e6, bar.get_y() + bar.get_height()/2, f'{width/1e6:.1f}M', ha='left', va='center', fontsize=9)
plt.tight_layout()

# Gráfico 3: Lucro (Linha Cronológica)
df_sorted_ano = df.sort_values("ano")
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.plot(df_sorted_ano["filme"], df_sorted_ano["lucro_corrigido"], color='#F5A623', marker='o', linestyle='-')
ax3.set_title('Evolução do Lucro Corrigido por Filme (Valores de 2025)', fontsize=16, pad=20)
ax3.set_ylabel('Lucro (em milhões de USD)', fontsize=12)
ax3.yaxis.set_major_formatter(lambda x, p: f'{x/1e6:.0f}M')
plt.xticks(rotation=45, ha="right")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()

plt.show()

# --- 6. Identificar destaques ---
maior_orcamento = df.loc[df["orcamento"].idxmax(), "filme"]
maior_bilheteria = df.loc[df["bilheteria"].idxmax(), "filme"]
maior_lucro = df.loc[df["lucro"].idxmax(), "filme"]

print("--- Análise de Vendas da Franquia (Valores Nominais) ---")
print(f"Filme com o maior orçamento: {maior_orcamento}")
print(f"Filme com a maior bilheteria: {maior_bilheteria}")
print(f"Filme com o maior lucro: {maior_lucro}")

# Salva o DataFrame completo em um arquivo CSV
df.to_csv('tabela_final_star_wars.csv', index=False, sep=';')

print("--- Tabela salva com sucesso no arquivo 'tabela_final_star_wars.csv' ---")
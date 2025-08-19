"use client";

import { useState } from "react";

const Home: React.FC = () => {
  // Estado inicial: matriz 4x4 preenchida com 0
  const [matrix, setMatrix] = useState<number[][]>(Array(4).fill(Array(4).fill(0)));
  const [resultadoPrevisao, setResultadoPrevisao] = useState<string | null>(null);

  // Função para alternar valor da célula
  const toggleCell = (row: number, col: number) => {
    const newMatrix = matrix.map((r, i) =>
      r.map((cell, j) => (i === row && j === col ? (cell === 0 ? 1 : 0) : cell))
    );
    setMatrix(newMatrix);
  };

  // Enviar para a API Flask
  const handlePredict = async () => {
    try {
      const res = await fetch("http://localhost:5000/prever", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matriz: matrix }),
      });

      const data = await res.json();
      alert(`resultado da previsão: ${data.previsao}`);
      setResultadoPrevisao(data.previsao);
    } catch (error) {
      console.error("Erro ao prever:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-black">
      <h1 className="text-4xl font-bold mb-2">Bem-vindo à Rede Neural</h1>
      <p className="text-lg mb-10">
        Clique nos quadrados para formar o dígito. Depois envie para a rede.
      </p>

      <div className="grid grid-cols-4 gap-2 mb-6">
        {matrix.map((row, i) =>
          row.map((cell, j) => (
            <button
              key={`${i}-${j}`}
              onClick={() => toggleCell(i, j)}
              className={`w-12 h-12 rounded ${cell === 1 ? "bg-blue-400" : "bg-black"}`}
            />
          ))
        )}
      </div>

      <button
        onClick={handlePredict}
        className="px-6 py-2 bg-green-500 text-white font-semibold rounded"
      >
        Enviar para Rede Neural
      </button>

      {resultadoPrevisao !== null && <p>Resultado da previsão: {resultadoPrevisao}</p>}
    </div>
  );
};

export default Home;

"use client";
import { motion } from "framer-motion";

import { useState } from "react";

const Home: React.FC = () => {
  // Estado inicial: matriz 4x4 preenchida com 0
  const [matrix, setMatrix] = useState<number[][]>(Array(4).fill(Array(4).fill(0)));
  const [resultadoPrevisao, setResultadoPrevisao] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [epochs, SetEpochs] = useState<number | null>(null);
  const [isTraining, setIsTraining] = useState<boolean>(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [meanSquaredErrors, setMeanSquaredErrors] = useState<Array<{ [key: number]: number }>>([]);

  // Função para alternar valor da célula
  const toggleCell = (row: number, col: number) => {
    const newMatrix = matrix.map((r, i) =>
      r.map((cell, j) => (i === row && j === col ? (cell === 0 ? 1 : 0) : cell))
    );
    setMatrix(newMatrix);
  };

  // Enviar para a API Flask
  const handleIdentify = async () => {
    setError(null);
    setIsTraining(false);
    setSuccessMessage(null);
    setMeanSquaredErrors([]);
    try {
      const res = await fetch("http://localhost:5000/identificar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ matriz: matrix }),
      });

      const data = await res.json();

      if (!res.ok) {
        // trata erro do backend
        setError(data.erro || "Ocorreu um erro ao identificar o dígito");
        return;
      }

      switch (data.previsao) {
        case 0:
          setResultadoPrevisao("0");
          break;
        case 1:
          setResultadoPrevisao("1");
          break;
        case 2:
          setResultadoPrevisao("4");
          break;
      }
    } catch (error) {
      console.error("Erro ao identificar o dígito:", error);
    }
  };

  const toggleTrain = () => {
    setError(null);
    setResultadoPrevisao(null);
    setIsTraining(!isTraining);
  };

  const handleTrain = async () => {
    setError(null);
    if (!epochs) return;

    try {
      const res = await fetch("http://localhost:5000/treinar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ epochs }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.erro || "Ocorreu um erro ao treinar");
        return;
      }

      SetEpochs(null);
      setIsTraining(false);
      setSuccessMessage(data.sucesso);
      setMeanSquaredErrors(data.mean_squared_errors);
    } catch (error) {
      console.error("Erro ao treinar:", error);
    }
  };

  const handleClean = () => {
    setMatrix(Array(4).fill(Array(4).fill(0)));
    setResultadoPrevisao(null);
    setError(null);
    setMeanSquaredErrors([]);
    setSuccessMessage(null);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-black py-30">
      <div className="max-w-[1024px] mx-auto">
        {successMessage && (
          <motion.p
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-green-500 mb-5 font-bold text-2xl text-center"
          >
            {successMessage}
          </motion.p>
        )}
        <motion.h1
          initial={{ opacity: 0, x: -50 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="text-4xl font-bold mb-2 text-center"
        >
          Bem-vindo à Rede Neural
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, x: -50 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="text-lg mb-10 text-center"
        >
          Clique nos quadrados para formar o dígito. Depois envie para a rede.
        </motion.p>
        <div className="flex flex-col items-center">
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="grid grid-cols-4 gap-2 mb-10"
          >
            {matrix.map((row, i) =>
              row.map((cell, j) => (
                <motion.button
                  initial={{ opacity: 0, y: -50 }}
                  animate={{
                    scale: cell === 1 ? 1.1 : 1,

                    transition: { duration: 0.2, ease: "easeInOut" },
                  }}
                  whileInView={{
                    opacity: 1,
                    y: 0,
                    transition: { duration: 0.9, ease: "easeInOut" },
                  }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95, rotate: 3 }}
                  key={`${i}-${j}`}
                  onClick={() => toggleCell(i, j)}
                  className={`w-12 h-12 rounded ${cell === 1 ? "bg-blue-400" : "bg-black"}`}
                />
              ))
            )}
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex gap-2 mb-5 justify-center"
        >
          <motion.button
            whileHover={{ scale: 1.03 }}
            onClick={handleIdentify}
            className="px-6 py-2 bg-green-500 text-white font-semibold rounded cursor-pointer"
          >
            Enviar para Rede Neural
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.03 }}
            className="px-6 py-2 bg-red-500 text-white font-semibold rounded cursor-pointer"
            onClick={() => handleClean()}
          >
            Limpar Matriz
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.03 }}
            className="px-6 py-2 bg-blue-500 text-white font-semibold rounded cursor-pointer"
            onClick={() => toggleTrain()}
          >
            Treinar Rede
          </motion.button>
        </motion.div>

        {resultadoPrevisao !== null && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            <p className="text-xl">
              Resultado da previsão:{" "}
              <motion.span
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                {resultadoPrevisao}
              </motion.span>
            </p>
          </motion.div>
        )}

        {error && (
          <div className="text-center">
            <p className="text-red-500">Erro: {error}</p>
          </div>
        )}

        {isTraining && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            transition={{ duration: 0.5 }}
            className="mt-5"
          >
            <p className="text-blue-500 text-center mb-2 text-md">Treinando a rede neural...</p>
            <motion.div className="text-center">
              <p className="">Número de épocas:</p>
              <input
                type="number"
                value={Number(epochs)}
                onChange={(e) => SetEpochs(Number(e.target.value))}
                className="border border-gray-300 rounded"
                placeholder="Determine o número de épocas"
              />
              <button
                className="ml-2 px-2 bg-green-500 rounded text-white cursor-pointer"
                onClick={() => handleTrain()}
              >
                Treinar
              </button>
            </motion.div>
          </motion.div>
        )}

        {meanSquaredErrors.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            transition={{ duration: 0.5 }}
            className="mt-10 p-5 bg-gray-300 rounded-2xl w-100 mx-auto"
          >
            <h3 className="text-lg font-semibold mb-2 text-center">
              Erros Médios Quadráticos (MSE)
            </h3>
            <ul className="list-disc list-inside">
              {meanSquaredErrors.map((error, index) => (
                <li key={index}>
                  Época {Object.keys(error)[0]}: {Object.values(error)[0]}
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Home;

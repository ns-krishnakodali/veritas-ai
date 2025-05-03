export const VeritasPage = () => {
  return (
    <div className="flex flex-col items-center justify-center text-center py-10">
      <h1 className="text-4xl font-bold mb-2">Veritas AI</h1>
      <p className="text-lg text-gray-600">
        A RAG model as a personal assistant
      </p>
      <div className="w-full px-4 py-3 shadow-md fixed bottom-0">
        <div className="max-w-2xl mx-auto flex">
          <input
            type="text"
            placeholder="Ask Veritas AI..."
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );
};

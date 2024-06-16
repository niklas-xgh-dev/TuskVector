import Image from "next/image";

export default async function Home() {
  const response = await fetch("http://localhost:8000/api/data");
  const data = await response.json();

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      {/* ... */}
      <div className="mb-32 grid text-center lg:mb-0 lg:w-full lg:max-w-5xl lg:grid-cols-4 lg:text-left">
        {/* ... */}
        <div>
          <h2 className="mb-3 text-2xl font-semibold">Data from Backend</h2>
          <p className="m-0 max-w-[30ch] text-balance text-sm opacity-50">{data.message}</p>
        </div>
      </div>
    </main>
  );
}
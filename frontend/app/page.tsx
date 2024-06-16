import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="mb-32 grid text-center lg:mb-0 lg:w-full lg:max-w-5xl lg:grid-cols-4 lg:text-left">
        <div>
          <h2 className="mb-3 text-2xl font-semibold">API Documentation</h2>
          <p>
            Check out our{" "}
            <a href="/docs" className="text-blue-500 underline">
              API Documentation
            </a>{" "}
            for more information on how to use our API.
          </p>
        </div>
      </div>
    </main>
  );
}
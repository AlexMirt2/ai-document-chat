interface MainLayoutProps {
  sidebar: React.ReactNode;
  content: React.ReactNode;
}

export default function MainLayout({
  sidebar,
  content,
}: MainLayoutProps) {
  return (
    <div className="flex h-screen bg-slate-900 text-white">

      {sidebar}

      <main className="flex-1 flex flex-col">

        {content}

      </main>

    </div>
  );
}
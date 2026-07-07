import MainLayout from "../components/layout/MainLayout";
import Sidebar from "../components/layout/Sidebar";
import MainContent from "../components/layout/MainContent";

export default function Dashboard() {
  return (
    <MainLayout
      sidebar={<Sidebar />}
      content={<MainContent />}
    />
  );
}
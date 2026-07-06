import MainLayout from "../components/layout/MainLayout";
import Sidebar from "../components/layout/Sidebar";
import ChatWindow from "../components/chat/ChatWindow";

export default function Dashboard() {
  return (
    <MainLayout
      sidebar={<Sidebar />}
      content={<ChatWindow />}
    />
  );
}
import { Video } from 'lucide-react';
import { FaGithub } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 p-6 backdrop-blur-sm bg-white/50 z-50 border-b border-emerald-100/20">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <Video className="text-emerald-600" />
          <span className="text-xl font-semibold text-gray-800">PitchPerfect</span>
        </div>
        <div className="flex space-x-8">
          <a href="https://github.com/LMol-4/Team36HackIreland" className="text-gray-600 hover:text-emerald-600 transition-colors flex items-center space-x-2">
            <FaGithub />
            <span>Github</span>
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
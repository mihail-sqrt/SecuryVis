import { useNavigate } from 'react-router-dom';
import MailIcon from '../icons/mail.svg';
import Mail from '../icons/Mail';
import User from '../icons/User';
import Logout from '../icons/Logout';
import { logout } from '../utils/backend';
import PenWrite from '../icons/PenWrite';
import CameraIcon from '../icons/CameraIcon';
import { useContext } from 'react';
import UserContext from '../contexts/UserContext';
import StaffIcon from '../icons/StaffIcon';
import LogsIcon from '../icons/LogsIcon';
import EnterpriseIcon from '../icons/EnterpriseIcon';

function VerticalHeader({ children }: any) {
    const navigate = useNavigate();
    const userData = useContext(UserContext);
    const url = window.location.pathname;

    return (
        <div className="h-screen flex flex-row align-top z-[99]">
            <header className="w-[100px] h-full flex fixed left-0 flex-col justify-start items-center px-5 bg-white shadow-sm pt-[80px]">
                <div onClick={() => navigate("/user")} className={`p-[20px] rounded-full cursor-pointer ${url == '/user' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <User />
                </div>
                <div onClick={() => navigate("/camera")} className={`p-[20px] rounded-full cursor-pointer ${url == '/camera' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <CameraIcon />
                </div>
                {
                    userData?.type == 'admin' &&
                    <div onClick={() => navigate("/enterprises")} className={`p-[20px] rounded-full cursor-pointer ${url == '/enterprises' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <EnterpriseIcon />
                </div>}
                <div onClick={() => navigate("/staff")} className={`p-[20px] rounded-full cursor-pointer ${url == '/staff' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <StaffIcon />
                </div>
                <div onClick={() => navigate("/logs")} className={`p-[20px] rounded-full cursor-pointer ${url == '/logs' ? 'text-white bg-[#0067E3]' : 'text-black'}`} >
                    <LogsIcon />
                </div>
                <div onClick={() => logout()} className={`p-[20px] rounded-full cursor-pointer mt-auto mb-2 text-black`} >
                    <Logout />
                </div>
            </header>
            <div className='w-[100px]'></div>
            <div className='w-full pt-[68px]'>
                {children}
            </div>
        </div>
    )
}

export default VerticalHeader;
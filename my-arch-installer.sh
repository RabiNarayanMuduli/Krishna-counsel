#!/data/data/com.termux/files/usr/bin/bash
#######################################################
#  📱 MOBILE ARCH DESKTOP - Ultimate Installer v3.1
#  XFCE4 + Termux-X11 + GPU + Audio
#  Clean Developer Edition
#######################################################

TOTAL_STEPS=10
CURRENT_STEP=0

GREEN='\033[0;32m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
YELLOW='\033[1;33m'
GRAY='\033[0;90m'
NC='\033[0m'

update_progress() {
    CURRENT_STEP=$((CURRENT_STEP + 1))
    PERCENT=$((CURRENT_STEP * 100 / TOTAL_STEPS))
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}  Step ${CURRENT_STEP}/${TOTAL_STEPS}  →  ${PERCENT}%${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

clear
echo -e "${CYAN}"
echo "╔══════════════════════════════════════╗"
echo "║     🚀 MOBILE ARCH DESKTOP 🚀       ║"
echo "║       Developer Edition v3.1        ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"
echo ""
read -p "Press Enter to start installation..."

#################################################
# STEP 1 - Update Termux
#################################################
update_progress
pkg update -y && pkg upgrade -y

#################################################
# STEP 2 - Install Required Packages
#################################################
update_progress
pkg install -y x11-repo
pkg install -y proot-distro termux-x11-nightly \
mesa-zink mesa-vulkan-icd-freedreno \
vulkan-loader-android pulseaudio git

#################################################
# STEP 3 - Install Arch Linux
#################################################
update_progress
proot-distro install archlinux || true

#################################################
# STEP 4 - Initialize Arch
#################################################
update_progress
proot-distro login archlinux -- bash -c "
pacman-key --init
pacman-key --populate archlinux
pacman -Syu --noconfirm
"

#################################################
# STEP 5 - Install Desktop Environment
#################################################
update_progress
proot-distro login archlinux -- bash -c "
pacman -S --noconfirm \
xfce4 xfce4-terminal thunar \
dbus networkmanager
"

#################################################
# STEP 6 - Install Applications (Inside Arch)
#################################################
update_progress
proot-distro login archlinux -- bash -c "
pacman -S --noconfirm \
firefox \
neovim \
base-devel \
code \
vlc \
htop
"

#################################################
# STEP 7 - GPU Acceleration Setup
#################################################
update_progress
mkdir -p ~/.config
cat > ~/.config/arch-gpu.sh << 'EOF'
export MESA_NO_ERROR=1
export GALLIUM_DRIVER=zink
export MESA_GL_VERSION_OVERRIDE=4.6
export MESA_GLES_VERSION_OVERRIDE=3.2
export MESA_LOADER_DRIVER_OVERRIDE=zink
export TU_DEBUG=noconform
export MESA_VK_WSI_PRESENT_MODE=immediate
EOF

#################################################
# STEP 8 - Create Launcher Script
#################################################
update_progress
cat > ~/start-arch.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Starting Mobile Arch Desktop..."

pkill -9 -f termux.x11 2>/dev/null
pkill -9 -f pulseaudio 2>/dev/null

pulseaudio --start --exit-idle-time=-1
export PULSE_SERVER=127.0.0.1

termux-x11 :0 -ac &
sleep 3

proot-distro login archlinux -- bash -c "
export DISPLAY=:0
export PULSE_SERVER=127.0.0.1
source ~/.config/arch-gpu.sh 2>/dev/null
dbus-launch startxfce4
"
EOF

chmod +x ~/start-arch.sh

#################################################
# STEP 9 - Create Stop Script
#################################################
update_progress
cat > ~/stop-arch.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
pkill -9 -f termux.x11
pkill -9 -f pulseaudio
pkill -9 -f xfce
echo "Desktop stopped."
EOF

chmod +x ~/stop-arch.sh

#################################################
# STEP 10 - Complete
#################################################
update_progress

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       ✅ INSTALLATION COMPLETE!      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "${WHITE}To Start Desktop:${NC}"
echo -e "${GREEN}  bash ~/start-arch.sh${NC}"
echo ""
echo -e "${WHITE}Open Termux-X11 app first.${NC}"
echo ""

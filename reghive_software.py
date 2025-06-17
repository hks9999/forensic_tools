from Registry import Registry
import datetime
import pytz

# SOFTWARE 하이브 경로
hive_path = "SOFTWARE"
reg = Registry.Registry(hive_path)

# 1. Windows 버전 및 설치 정보
def get_windows_version():
    key = reg.open(r"Microsoft\Windows NT\CurrentVersion")
    product_name = key.value("ProductName").value()
    edition = key.value("EditionID").value()
    version = key.value("CurrentVersion").value()
    build = key.value("CurrentBuildNumber").value()
    build_lab = key.value("BuildLab").value()
    install_ts = key.value("InstallDate").value()
    
    # UTC → KST (Asia/Seoul)로 변환
    install_dt = datetime.datetime.utcfromtimestamp(install_ts).replace(tzinfo=pytz.utc)
    kst = pytz.timezone("Asia/Seoul")
    install_dt_kst = install_dt.astimezone(kst)

    return {
        "ProductName": product_name,
        "EditionID": edition,
        "CurrentVersion": version,
        "CurrentBuildNumber": build,
        "BuildLab": build_lab,
        "InstallDate (KST)": install_dt_kst.strftime("%Y-%m-%d %H:%M:%S")
    }

# 2. 설치된 프로그램 정보
def get_installed_programs():
    key = reg.open(r"Microsoft\Windows\CurrentVersion\Uninstall")
    programs = []
    for subkey in key.subkeys():
        program_name = subkey.name()
        try:
            install_date = subkey.value("InstallDate").value()
            install_date = datetime.datetime.strptime(str(install_date), "%Y%m%d").date()
        except KeyError:
            install_date = "Unknown"
        programs.append({"Program": program_name, "InstallDate": install_date})

    return programs

# 3. 자동 실행 프로그램 (Run, RunOnce)
def get_auto_start_programs():
    key_run = reg.open(r"Microsoft\Windows\CurrentVersion\Run")
    key_runonce = reg.open(r"Microsoft\Windows\CurrentVersion\RunOnce")
    
    auto_start = {
        "Run": [],
        "RunOnce": []
    }
    
    # Run 프로그램
    for value in key_run.values():
        auto_start["Run"].append(value.name())
        
    # RunOnce 프로그램
    for value in key_runonce.values():
        auto_start["RunOnce"].append(value.name())
    
    return auto_start

# 4. 사용자 계정 정보 (ProfileList)
def get_user_accounts():
    key = reg.open(r"Microsoft\Windows NT\CurrentVersion\ProfileList")
    user_accounts = []
    for subkey in key.subkeys():
        sid = subkey.name()
        profile_path = subkey.value("ProfileImagePath").value()
        user_accounts.append({"SID": sid, "ProfilePath": profile_path})
    
    return user_accounts

# 5. 최근 사용된 프로그램 (MUICache, AppCompatCache)
def get_recently_used_programs():
    key_mui = reg.open(r"Microsoft\Windows\ShellNoRoam\MUICache")
    key_compat = reg.open(r"Microsoft\Windows\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store")
    
    recent_programs = {
        "MUICache": [],
        "AppCompatCache": []
    }
    
    # MUICache 프로그램
    for value in key_mui.values():
        recent_programs["MUICache"].append(value.name())
        
    # AppCompatCache 프로그램
    for value in key_compat.values():
        recent_programs["AppCompatCache"].append(value.name())
    
    return recent_programs

# 6. 설치된 드라이버 및 서비스 정보
def get_installed_drivers_and_services():
    key = reg.open(r"System\CurrentControlSet\Services")
    services = []
    for subkey in key.subkeys():
        services.append(subkey.name())
    
    return services

# 7. 타임존 및 지역 설정
def get_timezone_and_locale():
    key = reg.open(r"Control Panel\International")
    locale = key.value("Locale").value() if key.has_value("Locale") else "Unknown"
    timezone = key.value("TimeZone").value() if key.has_value("TimeZone") else "Unknown"
    
    return {"Locale": locale, "TimeZone": timezone}

# 8. USB 및 외부 디바이스 정보 (주로 SYSTEM 하이브에 있음, 그러나 SOFTWARE에서도 일부 확인 가능)
def get_usb_devices():
    key = reg.open(r"Microsoft\Windows\CurrentVersion\Explorer\Advanced")
    usb_devices = []
    try:
        for value in key.values():
            usb_devices.append(value.name())
    except Exception:
        pass
    return usb_devices

# 모든 정보를 파싱하여 출력
def parse_forensic_info():
    print("### 1. Windows Version & Install Info ###")
    windows_info = get_windows_version()
    for k, v in windows_info.items():
        print(f"{k}: {v}")
    '''
    print("\n### 2. Installed Programs ###")
    programs = get_installed_programs()
    for program in programs:
        print(f"Program: {program['Program']}, InstallDate: {program['InstallDate']}")
    '''
    
    
    '''
    print("\n### 3. Auto-Start Programs ###")
    auto_start = get_auto_start_programs()
    for category, programs in auto_start.items():
        print(f"{category}: {', '.join(programs)}")
    '''
    print("\n### 4. User Accounts ###")
    user_accounts = get_user_accounts()
    for account in user_accounts:
        print(f"SID: {account['SID']}, ProfilePath: {account['ProfilePath']}")
    '''
    print("\n### 5. Recently Used Programs ###")
    recent_programs = get_recently_used_programs()
    for category, programs in recent_programs.items():
        print(f"{category}: {', '.join(programs)}")
    '''
    '''
    print("\n### 6. Installed Drivers & Services ###")
    services = get_installed_drivers_and_services()
    print(f"Installed Services: {', '.join(services)}")
    '''
    '''
    print("\n### 7. TimeZone & Locale Settings ###")
    timezone_locale = get_timezone_and_locale()
    print(f"Locale: {timezone_locale['Locale']}, TimeZone: {timezone_locale['TimeZone']}")
    '''
    print("\n### 8. USB Devices ###")
    usb_devices = get_usb_devices()
    if usb_devices:
        print(f"USB Devices: {', '.join(usb_devices)}")
    else:
        print("No USB device data found in SOFTWARE.")

# 실행
parse_forensic_info()

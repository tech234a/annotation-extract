# Based on https://stackoverflow.com/questions/29266605, https://stackoverflow.com/questions/38309395

print("Initializing...")

from os import system, environ
import heroku3, tarfile
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET
from time import sleep

#From https://github.com/iv-org/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L79
CHARS_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

system("git config --global user.name \"annotation-extract-bot\"")
system("git config --global user.email annotation-extract-bot@annotation-extract-bot.local")

url = environ["url"] # ex https://archive.org/download/youtubeannotations_00/A-.tar
print(url)
itema = environ["url"].split("/")[-1].split(".")[0]

print("Downloading tar file (this may take a while)...")
urlretrieve(url, url.split("/")[-1])

print("Extracting tar file...")
tar = tarfile.open(url.split("/")[-1])

vidsl = set()
urlsl = set()
yturl = set()

# https://stackoverflow.com/a/19587581
for file in tar:
    if file:
        myfi = tar.extractfile(file)
        if myfi:
            try:
                urls = ET.parse(myfi).getroot().findall('.//url')
                for tag in urls:
                    urlint = tag.attrib['value']
                    if urlint.startswith("https://www.youtube.com/watch?"):
                        vidsl.add(urlint.split("v=")[-1].split("&")[0].split("#")[0])
                    elif urlint.startswith("https://www.youtube.com/"):
                        yturl.add(urlint.removeprefix("https://www.youtube.com/"))
                    else:
                        urlsl.add(urlint)
            except:
                print("error", file)

system("git clone "+environ["git-url"]+" repo")
urlf = open("repo/"+itema+"_urls.txt", "w")
for item in urlsl:
    urlf.write(item+"\n")
urlf.close()

vidf = open("repo/"+itema+"_vids.txt", "w")
for item in vidsl:
    vidf.write(item+"\n")
vidf.close()

yturlf = open("repo/"+itema+"_yturls.txt", "w")
for item in yturl:
    yturlf.write(item+"\n")
yturlf.close()

system("cd repo; git add .; git commit -m \"Add "+itema+"\"; git push")

applist = heroku3.from_key(environ['heroku-key']).apps(order_by="name")
currentlists = []
for app in applist:
    if app.name.startswith("annotation"):
        currentlists.append(app.config()["url"].split("/")[-1].split(".")[0])
        
todoitems = ['--', '-0', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', '-9', '-A', '-B', '-C', '-D', '-E', '-F', '-G', '-H', '-I', '-J', '-K', '-L', '-M', '-N', '-O', '-P', '-Q', '-R', '-S', '-T', '-U', '-V', '-W', '-X', '-Y', '-Z', '-_', '-a', '-b', '-c', '-d', '-e', '-f', '-g', '-h', '-i', '-j', '-k', '-l', '-m', '-n', '-o', '-p', '-q', '-r', '-s', '-t', '-u', '-v', '-w', '-x', '-y', '-z', '0-', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B', '0C', '0D', '0E', '0F', '0G', '0H', '0I', '0J', '0K', '0L', '0M', '0N', '0O', '0P', '0Q', '0R', '0S', '0T', '0U', '0V', '0W', '0X', '0Y', '0Z', '0_', '0a', '0b', '0c', '0d', '0e', '0f', '0g', '0h', '0i', '0j', '0k', '0l', '0m', '0n', '0o', '0p', '0q', '0r', '0s', '0t', '0u', '0v', '0w', '0x', '0y', '0z', '1-', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L', '1M', '1N', '1O', '1P', '1Q', '1R', '1S', '1T', '1U', '1V', '1W', '1X', '1Y', '1Z', '1_', '1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h', '1i', '1j', '1k', '1l', '1m', '1n', '1o', '1p', '1q', '1r', '1s', '1t', '1u', '1v', '1w', '1x', '1y', '1z', '2-', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L', '2M', '2N', '2O', '2P', '2Q', '2R', '2S', '2T', '2U', '2V', '2W', '2X', '2Y', '2Z', '2_', '2a', '2b', '2c', '2d', '2e', '2f', '2g', '2h', '2i', '2j', '2k', '2l', '2m', '2n', '2o', '2p', '2q', '2r', '2s', '2t', '2u', '2v', '2w', '2x', '2y', '2z', '3-', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F', '3G', '3H', '3I', '3J', '3K', '3L', '3M', '3N', '3O', '3P', '3Q', '3R', '3S', '3T', '3U', '3V', '3W', '3X', '3Y', '3Z', '3_', '3a', '3b', '3c', '3d', '3e', '3f', '3g', '3h', '3i', '3j', '3k', '3l', '3m', '3n', '3o', '3p', '3q', '3r', '3s', '3t', '3u', '3v', '3w', '3x', '3y', '3z', '4-', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F', '4G', '4H', '4I', '4J', '4K', '4L', '4M', '4N', '4O', '4P', '4Q', '4R', '4S', '4T', '4U', '4V', '4W', '4X', '4Y', '4Z', '4_', '4a', '4b', '4c', '4d', '4e', '4f', '4g', '4h', '4i', '4j', '4k', '4l', '4m', '4n', '4o', '4p', '4q', '4r', '4s', '4t', '4u', '4v', '4w', '4x', '4y', '4z', '5-', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5A', '5B', '5C', '5D', '5E', '5F', '5G', '5H', '5I', '5J', '5K', '5L', '5M', '5N', '5O', '5P', '5Q', '5R', '5S', '5T', '5U', '5V', '5W', '5X', '5Y', '5Z', '5_', '5a', '5b', '5c', '5d', '5e', '5f', '5g', '5h', '5i', '5j', '5k', '5l', '5m', '5n', '5o', '5p', '5q', '5r', '5s', '5t', '5u', '5v', '5w', '5x', '5y', '5z', '6-', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D', '6E', '6F', '6G', '6H', '6I', '6J', '6K', '6L', '6M', '6N', '6O', '6P', '6Q', '6R', '6S', '6T', '6U', '6V', '6W', '6X', '6Y', '6Z', '6_', '6a', '6b', '6c', '6d', '6e', '6f', '6g', '6h', '6i', '6j', '6k', '6l', '6m', '6n', '6o', '6p', '6q', '6r', '6s', '6t', '6u', '6v', '6w', '6x', '6y', '6z', '7-', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '7G', '7H', '7I', '7J', '7K', '7L', '7M', '7N', '7O', '7P', '7Q', '7R', '7S', '7T', '7U', '7V', '7W', '7X', '7Y', '7Z', '7_', '7a', '7b', '7c', '7d', '7e', '7f', '7g', '7h', '7i', '7j', '7k', '7l', '7m', '7n', '7o', '7p', '7q', '7r', '7s', '7t', '7u', '7v', '7w', '7x', '7y', '7z', '8-', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B', '8C', '8D', '8E', '8F', '8G', '8H', '8I', '8J', '8K', '8L', '8M', '8N', '8O', '8P', '8Q', '8R', '8S', '8T', '8U', '8V', '8W', '8X', '8Y', '8Z', '8_', '8a', '8b', '8c', '8d', '8e', '8f', '8g', '8h', '8i', '8j', '8k', '8l', '8m', '8n', '8o', '8p', '8q', '8r', '8s', '8t', '8u', '8v', '8w', '8x', '8y', '8z', '9-', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F', '9G', '9H', '9I', '9J', '9K', '9L', '9M', '9N', '9O', '9P', '9Q', '9R', '9S', '9T', '9U', '9V', '9W', '9X', '9Y', '9Z', '9_', '9a', '9b', '9c', '9d', '9e', '9f', '9g', '9h', '9i', '9j', '9k', '9l', '9m', '9n', '9o', '9p', '9q', '9r', '9s', '9t', '9u', '9v', '9w', '9x', '9y', '9z', 'A-', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'A_', 'Aa', 'Ab', 'Ac', 'Ad', 'Ae', 'Af', 'Ag', 'Ah', 'Ai', 'Aj', 'Ak', 'Al', 'Am', 'An', 'Ao', 'Ap', 'Aq', 'Ar', 'As', 'At', 'Au', 'Av', 'Aw', 'Ax', 'Ay', 'Az', 'B-', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'B_', 'Ba', 'Bb', 'Bc', 'Bd', 'Be', 'Bf', 'Bg', 'Bh', 'Bi', 'Bj', 'Bk', 'Bl', 'Bm', 'Bn', 'Bo', 'Bp', 'Bq', 'Br', 'Bs', 'Bt', 'Bu', 'Bv', 'Bw', 'Bx', 'By', 'Bz', 'C-', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'C_', 'Ca', 'Cb', 'Cc', 'Cd', 'Ce', 'Cf', 'Cg', 'Ch', 'Ci', 'Cj', 'Ck', 'Cl', 'Cm', 'Cn', 'Co', 'Cp', 'Cq', 'Cr', 'Cs', 'Ct', 'Cu', 'Cv', 'Cw', 'Cx', 'Cy', 'Cz', 'D-', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX', 'DY', 'DZ', 'D_', 'Da', 'Db', 'Dc', 'Dd', 'De', 'Df', 'Dg', 'Dh', 'Di', 'Dj', 'Dk', 'Dl', 'Dm', 'Dn', 'Do', 'Dp', 'Dq', 'Dr', 'Ds', 'Dt', 'Du', 'Dv', 'Dw', 'Dx', 'Dy', 'Dz', 'E-', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF', 'EG', 'EH', 'EI', 'EJ', 'EK', 'EL', 'EM', 'EN', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ', 'E_', 'Ea', 'Eb', 'Ec', 'Ed', 'Ee', 'Ef', 'Eg', 'Eh', 'Ei', 'Ej', 'Ek', 'El', 'Em', 'En', 'Eo', 'Ep', 'Eq', 'Er', 'Es', 'Et', 'Eu', 'Ev', 'Ew', 'Ex', 'Ey', 'Ez', 'F-', 'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'FI', 'FJ', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP', 'FQ', 'FR', 'FS', 'FT', 'FU', 'FV', 'FW', 'FX', 'FY', 'FZ', 'F_', 'Fa', 'Fb', 'Fc', 'Fd', 'Fe', 'Ff', 'Fg', 'Fh', 'Fi', 'Fj', 'Fk', 'Fl', 'Fm', 'Fn', 'Fo', 'Fp', 'Fq', 'Fr', 'Fs', 'Ft', 'Fu', 'Fv', 'Fw', 'Fx', 'Fy', 'Fz', 'G-', 'G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'GA', 'GB', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM', 'GN', 'GO', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GV', 'GW', 'GX', 'GY', 'GZ', 'G_', 'Ga', 'Gb', 'Gc', 'Gd', 'Ge', 'Gf', 'Gg', 'Gh', 'Gi', 'Gj', 'Gk', 'Gl', 'Gm', 'Gn', 'Go', 'Gp', 'Gq', 'Gr', 'Gs', 'Gt', 'Gu', 'Gv', 'Gw', 'Gx', 'Gy', 'Gz', 'H-', 'H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HU', 'HV', 'HW', 'HX', 'HY', 'HZ', 'H_', 'Ha', 'Hb', 'Hc', 'Hd', 'He', 'Hf', 'Hg', 'Hh', 'Hi', 'Hj', 'Hk', 'Hl', 'Hm', 'Hn', 'Ho', 'Hp', 'Hq', 'Hr', 'Hs', 'Ht', 'Hu', 'Hv', 'Hw', 'Hx', 'Hy', 'Hz', 'I-', 'I0', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'IA', 'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK', 'IL', 'IM', 'IN', 'IO', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IU', 'IV', 'IW', 'IX', 'IY', 'IZ', 'I_', 'Ia', 'Ib', 'Ic', 'Id', 'Ie', 'If', 'Ig', 'Ih', 'Ii', 'Ij', 'Ik', 'Il', 'Im', 'In', 'Io', 'Ip', 'Iq', 'Ir', 'Is', 'It', 'Iu', 'Iv', 'Iw', 'Ix', 'Iy', 'Iz', 'J-', 'J0', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'JA', 'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH', 'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP', 'JQ', 'JR', 'JS', 'JT', 'JU', 'JV', 'JW', 'JX', 'JY', 'JZ', 'J_', 'Ja', 'Jb', 'Jc', 'Jd', 'Je', 'Jf', 'Jg', 'Jh', 'Ji', 'Jj', 'Jk', 'Jl', 'Jm', 'Jn', 'Jo', 'Jp', 'Jq', 'Jr', 'Js', 'Jt', 'Ju', 'Jv', 'Jw', 'Jx', 'Jy', 'Jz', 'K-', 'K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KV', 'KW', 'KX', 'KY', 'KZ', 'K_', 'Ka', 'Kb', 'Kc', 'Kd', 'Ke', 'Kf', 'Kg', 'Kh', 'Ki', 'Kj', 'Kk', 'Kl', 'Km', 'Kn', 'Ko', 'Kp', 'Kq', 'Kr', 'Ks', 'Kt', 'Ku', 'Kv', 'Kw', 'Kx', 'Ky', 'Kz', 'L-', 'L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'LA', 'LB', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LJ', 'LK', 'LL', 'LM', 'LN', 'LO', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LU', 'LV', 'LW', 'LX', 'LY', 'LZ', 'L_', 'La', 'Lb', 'Lc', 'Ld', 'Le', 'Lf', 'Lg', 'Lh', 'Li', 'Lj', 'Lk', 'Ll', 'Lm', 'Ln', 'Lo', 'Lp', 'Lq', 'Lr', 'Ls', 'Lt', 'Lu', 'Lv', 'Lw', 'Lx', 'Ly', 'Lz', 'M-', 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MJ', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'M_', 'Ma', 'Mb', 'Mc', 'Md', 'Me', 'Mf', 'Mg', 'Mh', 'Mi', 'Mj', 'Mk', 'Ml', 'Mm', 'Mn', 'Mo', 'Mp', 'Mq', 'Mr', 'Ms', 'Mt', 'Mu', 'Mv', 'Mw', 'Mx', 'My', 'Mz', 'N-', 'N0', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY', 'NZ', 'N_', 'Na', 'Nb', 'Nc', 'Nd', 'Ne', 'Nf', 'Ng', 'Nh', 'Ni', 'Nj', 'Nk', 'Nl', 'Nm', 'Nn', 'No', 'Np', 'Nq', 'Nr', 'Ns', 'Nt', 'Nu', 'Nv', 'Nw', 'Nx', 'Ny', 'Nz', 'O-', 'O0', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9', 'OA', 'OB', 'OC', 'OD', 'OE', 'OF', 'OG', 'OH', 'OI', 'OJ', 'OK', 'OL', 'OM', 'ON', 'OO', 'OP', 'OQ', 'OR', 'OS', 'OT', 'OU', 'OV', 'OW', 'OX', 'OY', 'OZ', 'O_', 'Oa', 'Ob', 'Oc', 'Od', 'Oe', 'Of', 'Og', 'Oh', 'Oi', 'Oj', 'Ok', 'Ol', 'Om', 'On', 'Oo', 'Op', 'Oq', 'Or', 'Os', 'Ot', 'Ou', 'Ov', 'Ow', 'Ox', 'Oy', 'Oz', 'P-', 'P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PJ', 'PK', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PU', 'PV', 'PW', 'PX', 'PY', 'PZ', 'P_', 'Pa', 'Pb', 'Pc', 'Pd', 'Pe', 'Pf', 'Pg', 'Ph', 'Pi', 'Pj', 'Pk', 'Pl', 'Pm', 'Pn', 'Po', 'Pp', 'Pq', 'Pr', 'Ps', 'Pt', 'Pu', 'Pv', 'Pw', 'Px', 'Py', 'Pz', 'Q-', 'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'QA', 'QB', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QJ', 'QK', 'QL', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU', 'QV', 'QW', 'QX', 'QY', 'QZ', 'Q_', 'Qa', 'Qb', 'Qc', 'Qd', 'Qe', 'Qf', 'Qg', 'Qh', 'Qi', 'Qj', 'Qk', 'Ql', 'Qm', 'Qn', 'Qo', 'Qp', 'Qq', 'Qr', 'Qs', 'Qt', 'Qu', 'Qv', 'Qw', 'Qx', 'Qy', 'Qz', 'R-', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'RA', 'RB', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RJ', 'RK', 'RL', 'RM', 'RN', 'RO', 'RP', 'RQ', 'RR', 'RS', 'RT', 'RU', 'RV', 'RW', 'RX', 'RY', 'RZ', 'R_', 'Ra', 'Rb', 'Rc', 'Rd', 'Re', 'Rf', 'Rg', 'Rh', 'Ri', 'Rj', 'Rk', 'Rl', 'Rm', 'Rn', 'Ro', 'Rp', 'Rq', 'Rr', 'Rs', 'Rt', 'Ru', 'Rv', 'Rw', 'Rx', 'Ry', 'Rz', 'S-', 'S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SQ', 'SR', 'SS', 'ST', 'SU', 'SV', 'SW', 'SX', 'SY', 'SZ', 'S_', 'Sa', 'Sb', 'Sc', 'Sd', 'Se', 'Sf', 'Sg', 'Sh', 'Si', 'Sj', 'Sk', 'Sl', 'Sm', 'Sn', 'So', 'Sp', 'Sq', 'Sr', 'Ss', 'St', 'Su', 'Sv', 'Sw', 'Sx', 'Sy', 'Sz', 'T-', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TP', 'TQ', 'TR', 'TS', 'TT', 'TU', 'TV', 'TW', 'TX', 'TY', 'TZ', 'T_', 'Ta', 'Tb', 'Tc', 'Td', 'Te', 'Tf', 'Tg', 'Th', 'Ti', 'Tj', 'Tk', 'Tl', 'Tm', 'Tn', 'To', 'Tp', 'Tq', 'Tr', 'Ts', 'Tt', 'Tu', 'Tv', 'Tw', 'Tx', 'Ty', 'Tz', 'U-', 'U0', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'UA', 'UB', 'UC', 'UD', 'UE', 'UF', 'UG', 'UH', 'UI', 'UJ', 'UK', 'UL', 'UM', 'UN', 'UO', 'UP', 'UQ', 'UR', 'US', 'UT', 'UU', 'UV', 'UW', 'UX', 'UY', 'UZ', 'U_', 'Ua', 'Ub', 'Uc', 'Ud', 'Ue', 'Uf', 'Ug', 'Uh', 'Ui', 'Uj', 'Uk', 'Ul', 'Um', 'Un', 'Uo', 'Up', 'Uq', 'Ur', 'Us', 'Ut', 'Uu', 'Uv', 'Uw', 'Ux', 'Uy', 'Uz', 'V-', 'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'VA', 'VB', 'VC', 'VD', 'VE', 'VF', 'VG', 'VH', 'VI', 'VJ', 'VK', 'VL', 'VM', 'VN', 'VO', 'VP', 'VQ', 'VR', 'VS', 'VT', 'VU', 'VV', 'VW', 'VX', 'VY', 'VZ', 'V_', 'Va', 'Vb', 'Vc', 'Vd', 'Ve', 'Vf', 'Vg', 'Vh', 'Vi', 'Vj', 'Vk', 'Vl', 'Vm', 'Vn', 'Vo', 'Vp', 'Vq', 'Vr', 'Vs', 'Vt', 'Vu', 'Vv', 'Vw', 'Vx', 'Vy', 'Vz', 'W-', 'W0', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL', 'WM', 'WN', 'WO', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WU', 'WV', 'WW', 'WX', 'WY', 'WZ', 'W_', 'Wa', 'Wb', 'Wc', 'Wd', 'We', 'Wf', 'Wg', 'Wh', 'Wi', 'Wj', 'Wk', 'Wl', 'Wm', 'Wn', 'Wo', 'Wp', 'Wq', 'Wr', 'Ws', 'Wt', 'Wu', 'Wv', 'Ww', 'Wx', 'Wy', 'Wz', 'X-', 'X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'XA', 'XB', 'XC', 'XD', 'XE', 'XF', 'XG', 'XH', 'XI', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XO', 'XP', 'XQ', 'XR', 'XS', 'XT', 'XU', 'XV', 'XW', 'XX', 'XY', 'XZ', 'X_', 'Xa', 'Xb', 'Xc', 'Xd', 'Xe', 'Xf', 'Xg', 'Xh', 'Xi', 'Xj', 'Xk', 'Xl', 'Xm', 'Xn', 'Xo', 'Xp', 'Xq', 'Xr', 'Xs', 'Xt', 'Xu', 'Xv', 'Xw', 'Xx', 'Xy', 'Xz', 'Y-', 'Y0', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'YA', 'YB', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YJ', 'YK', 'YL', 'YM', 'YN', 'YO', 'YP', 'YQ', 'YR', 'YS', 'YT', 'YU', 'YV', 'YW', 'YX', 'YY', 'YZ', 'Y_', 'Ya', 'Yb', 'Yc', 'Yd', 'Ye', 'Yf', 'Yg', 'Yh', 'Yi', 'Yj', 'Yk', 'Yl', 'Ym', 'Yn', 'Yo', 'Yp', 'Yq', 'Yr', 'Ys', 'Yt', 'Yu', 'Yv', 'Yw', 'Yx', 'Yy', 'Yz', 'Z-', 'Z0', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'ZA', 'ZB', 'ZC', 'ZD', 'ZE', 'ZF', 'ZG', 'ZH', 'ZI', 'ZJ', 'ZK', 'ZL', 'ZM', 'ZN', 'ZO', 'ZP', 'ZQ', 'ZR', 'ZS', 'ZT', 'ZU', 'ZV', 'ZW', 'ZX', 'ZY', 'ZZ', 'Z_', 'Za', 'Zb', 'Zc', 'Zd', 'Ze', 'Zf', 'Zg', 'Zh', 'Zi', 'Zj', 'Zk', 'Zl', 'Zm', 'Zn', 'Zo', 'Zp', 'Zq', 'Zr', 'Zs', 'Zt', 'Zu', 'Zv', 'Zw', 'Zx', 'Zy', 'Zz', '_-', '_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', '_A', '_B', '_C', '_D', '_E', '_F', '_G', '_H', '_I', '_J', '_K', '_L', '_M', '_N', '_O', '_P', '_Q', '_R', '_S', '_T', '_U', '_V', '_W', '_X', '_Y', '_Z', '__', '_a', '_b', '_c', '_d', '_e', '_f', '_g', '_h', '_i', '_j', '_k', '_l', '_m', '_n', '_o', '_p', '_q', '_r', '_s', '_t', '_u', '_v', '_w', '_x', '_y', '_z', 'a-', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aA', 'aB', 'aC', 'aD', 'aE', 'aF', 'aG', 'aH', 'aI', 'aJ', 'aK', 'aL', 'aM', 'aN', 'aO', 'aP', 'aQ', 'aR', 'aS', 'aT', 'aU', 'aV', 'aW', 'aX', 'aY', 'aZ', 'a_', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'b-', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'bA', 'bB', 'bC', 'bD', 'bE', 'bF', 'bG', 'bH', 'bI', 'bJ', 'bK', 'bL', 'bM', 'bN', 'bO', 'bP', 'bQ', 'bR', 'bS', 'bT', 'bU', 'bV', 'bW', 'bX', 'bY', 'bZ', 'b_', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk', 'bl', 'bm', 'bn', 'bo', 'bp', 'bq', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by', 'bz', 'c-', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'cA', 'cB', 'cC', 'cD', 'cE', 'cF', 'cG', 'cH', 'cI', 'cJ', 'cK', 'cL', 'cM', 'cN', 'cO', 'cP', 'cQ', 'cR', 'cS', 'cT', 'cU', 'cV', 'cW', 'cX', 'cY', 'cZ', 'c_', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci', 'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'd-', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'dA', 'dB', 'dC', 'dD', 'dE', 'dF', 'dG', 'dH', 'dI', 'dJ', 'dK', 'dL', 'dM', 'dN', 'dO', 'dP', 'dQ', 'dR', 'dS', 'dT', 'dU', 'dV', 'dW', 'dX', 'dY', 'dZ', 'd_', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds', 'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'e-', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'eA', 'eB', 'eC', 'eD', 'eE', 'eF', 'eG', 'eH', 'eI', 'eJ', 'eK', 'eL', 'eM', 'eN', 'eO', 'eP', 'eQ', 'eR', 'eS', 'eT', 'eU', 'eV', 'eW', 'eX', 'eY', 'eZ', 'e_', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ey', 'ez', 'f-', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fA', 'fB', 'fC', 'fD', 'fE', 'fF', 'fG', 'fH', 'fI', 'fJ', 'fK', 'fL', 'fM', 'fN', 'fO', 'fP', 'fQ', 'fR', 'fS', 'fT', 'fU', 'fV', 'fW', 'fX', 'fY', 'fZ', 'f_', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fg', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn', 'fo', 'fp', 'fq', 'fr', 'fs', 'ft', 'fu', 'fv', 'fw', 'fx', 'fy', 'fz', 'g-', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'gA', 'gB', 'gC', 'gD', 'gE', 'gF', 'gG', 'gH', 'gI', 'gJ', 'gK', 'gL', 'gM', 'gN', 'gO', 'gP', 'gQ', 'gR', 'gS', 'gT', 'gU', 'gV', 'gW', 'gX', 'gY', 'gZ', 'g_', 'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm', 'gn', 'go', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gy', 'gz', 'h-', 'h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'hA', 'hB', 'hC', 'hD', 'hE', 'hF', 'hG', 'hH', 'hI', 'hJ', 'hK', 'hL', 'hM', 'hN', 'hO', 'hP', 'hQ', 'hR', 'hS', 'hT', 'hU', 'hV', 'hW', 'hX', 'hY', 'hZ', 'h_', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hi', 'hj', 'hk', 'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw', 'hx', 'hy', 'hz', 'i-', 'i0', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'iA', 'iB', 'iC', 'iD', 'iE', 'iF', 'iG', 'iH', 'iI', 'iJ', 'iK', 'iL', 'iM', 'iN', 'iO', 'iP', 'iQ', 'iR', 'iS', 'iT', 'iU', 'iV', 'iW', 'iX', 'iY', 'iZ', 'i_', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii', 'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'iw', 'ix', 'iy', 'iz', 'j-', 'j0', 'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9', 'jA', 'jB', 'jC', 'jD', 'jE', 'jF', 'jG', 'jH', 'jI', 'jJ', 'jK', 'jL', 'jM', 'jN', 'jO', 'jP', 'jQ', 'jR', 'jS', 'jT', 'jU', 'jV', 'jW', 'jX', 'jY', 'jZ', 'j_', 'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg', 'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jq', 'jr', 'js', 'jt', 'ju', 'jv', 'jw', 'jx', 'jy', 'jz', 'k-', 'k0', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8', 'k9', 'kA', 'kB', 'kC', 'kD', 'kE', 'kF', 'kG', 'kH', 'kI', 'kJ', 'kK', 'kL', 'kM', 'kN', 'kO', 'kP', 'kQ', 'kR', 'kS', 'kT', 'kU', 'kV', 'kW', 'kX', 'kY', 'kZ', 'k_', 'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kp', 'kq', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'l-', 'l0', 'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'lA', 'lB', 'lC', 'lD', 'lE', 'lF', 'lG', 'lH', 'lI', 'lJ', 'lK', 'lL', 'lM', 'lN', 'lO', 'lP', 'lQ', 'lR', 'lS', 'lT', 'lU', 'lV', 'lW', 'lX', 'lY', 'lZ', 'l_', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'lk', 'll', 'lm', 'ln', 'lo', 'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lw', 'lx', 'ly', 'lz', 'm-', 'm0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'mA', 'mB', 'mC', 'mD', 'mE', 'mF', 'mG', 'mH', 'mI', 'mJ', 'mK', 'mL', 'mM', 'mN', 'mO', 'mP', 'mQ', 'mR', 'mS', 'mT', 'mU', 'mV', 'mW', 'mX', 'mY', 'mZ', 'm_', 'ma', 'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'n-', 'n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9', 'nA', 'nB', 'nC', 'nD', 'nE', 'nF', 'nG', 'nH', 'nI', 'nJ', 'nK', 'nL', 'nM', 'nN', 'nO', 'nP', 'nQ', 'nR', 'nS', 'nT', 'nU', 'nV', 'nW', 'nX', 'nY', 'nZ', 'n_', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nk', 'nl', 'nm', 'nn', 'no', 'np', 'nq', 'nr', 'ns', 'nt', 'nu', 'nv', 'nw', 'nx', 'ny', 'nz', 'o-', 'o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8', 'o9', 'oA', 'oB', 'oC', 'oD', 'oE', 'oF', 'oG', 'oH', 'oI', 'oJ', 'oK', 'oL', 'oM', 'oN', 'oO', 'oP', 'oQ', 'oR', 'oS', 'oT', 'oU', 'oV', 'oW', 'oX', 'oY', 'oZ', 'o_', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi', 'oj', 'ok', 'ol', 'om', 'on', 'oo', 'op', 'oq', 'or', 'os', 'ot', 'ou', 'ov', 'ow', 'ox', 'oy', 'oz', 'p-', 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'pA', 'pB', 'pC', 'pD', 'pE', 'pF', 'pG', 'pH', 'pI', 'pJ', 'pK', 'pL', 'pM', 'pN', 'pO', 'pP', 'pQ', 'pR', 'pS', 'pT', 'pU', 'pV', 'pW', 'pX', 'pY', 'pZ', 'p_', 'pa', 'pb', 'pc', 'pd', 'pe', 'pf', 'pg', 'ph', 'pi', 'pj', 'pk', 'pl', 'pm', 'pn', 'po', 'pp', 'pq', 'pr', 'ps', 'pt', 'pu', 'pv', 'pw', 'px', 'py', 'pz', 'q-', 'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'qA', 'qB', 'qC', 'qD', 'qE', 'qF', 'qG', 'qH', 'qI', 'qJ', 'qK', 'qL', 'qM', 'qN', 'qO', 'qP', 'qQ', 'qR', 'qS', 'qT', 'qU', 'qV', 'qW', 'qX', 'qY', 'qZ', 'q_', 'qa', 'qb', 'qc', 'qd', 'qe', 'qf', 'qg', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq', 'qr', 'qs', 'qt', 'qu', 'qv', 'qw', 'qx', 'qy', 'qz', 'r-', 'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'rA', 'rB', 'rC', 'rD', 'rE', 'rF', 'rG', 'rH', 'rI', 'rJ', 'rK', 'rL', 'rM', 'rN', 'rO', 'rP', 'rQ', 'rR', 'rS', 'rT', 'rU', 'rV', 'rW', 'rX', 'rY', 'rZ', 'r_', 'ra', 'rb', 'rc', 'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro', 'rp', 'rq', 'rr', 'rs', 'rt', 'ru', 'rv', 'rw', 'rx', 'ry', 'rz', 's-', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 'sA', 'sB', 'sC', 'sD', 'sE', 'sF', 'sG', 'sH', 'sI', 'sJ', 'sK', 'sL', 'sM', 'sN', 'sO', 'sP', 'sQ', 'sR', 'sS', 'sT', 'sU', 'sV', 'sW', 'sX', 'sY', 'sZ', 's_', 'sa', 'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'sx', 'sy', 'sz', 't-', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 'tA', 'tB', 'tC', 'tD', 'tE', 'tF', 'tG', 'tH', 'tI', 'tJ', 'tK', 'tL', 'tM', 'tN', 'tO', 'tP', 'tQ', 'tR', 'tS', 'tT', 'tU', 'tV', 'tW', 'tX', 'tY', 'tZ', 't_', 'ta', 'tb', 'tc', 'td', 'te', 'tf', 'tg', 'th', 'ti', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tq', 'tr', 'ts', 'tt', 'tu', 'tv', 'tw', 'tx', 'ty', 'tz', 'u-', 'u0', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9', 'uA', 'uB', 'uC', 'uD', 'uE', 'uF', 'uG', 'uH', 'uI', 'uJ', 'uK', 'uL', 'uM', 'uN', 'uO', 'uP', 'uQ', 'uR', 'uS', 'uT', 'uU', 'uV', 'uW', 'uX', 'uY', 'uZ', 'u_', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uh', 'ui', 'uj', 'uk', 'ul', 'um', 'un', 'uo', 'up', 'uq', 'ur', 'us', 'ut', 'uu', 'uv', 'uw', 'ux', 'uy', 'uz', 'v-', 'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'vA', 'vB', 'vC', 'vD', 'vE', 'vF', 'vG', 'vH', 'vI', 'vJ', 'vK', 'vL', 'vM', 'vN', 'vO', 'vP', 'vQ', 'vR', 'vS', 'vT', 'vU', 'vV', 'vW', 'vX', 'vY', 'vZ', 'v_', 'va', 'vb', 'vc', 'vd', 've', 'vf', 'vg', 'vh', 'vi', 'vj', 'vk', 'vl', 'vm', 'vn', 'vo', 'vp', 'vq', 'vr', 'vs', 'vt', 'vu', 'vv', 'vw', 'vx', 'vy', 'vz', 'w-', 'w0', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'wA', 'wB', 'wC', 'wD', 'wE', 'wF', 'wG', 'wH', 'wI', 'wJ', 'wK', 'wL', 'wM', 'wN', 'wO', 'wP', 'wQ', 'wR', 'wS', 'wT', 'wU', 'wV', 'wW', 'wX', 'wY', 'wZ', 'w_', 'wa', 'wb', 'wc', 'wd', 'we', 'wf', 'wg', 'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp', 'wq', 'wr', 'ws', 'wt', 'wu', 'wv', 'ww', 'wx', 'wy', 'wz', 'x-', 'x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'xA', 'xB', 'xC', 'xD', 'xE', 'xF', 'xG', 'xH', 'xI', 'xJ', 'xK', 'xL', 'xM', 'xN', 'xO', 'xP', 'xQ', 'xR', 'xS', 'xT', 'xU', 'xV', 'xW', 'xX', 'xY', 'xZ', 'x_', 'xa', 'xb', 'xc', 'xd', 'xe', 'xf', 'xg', 'xh', 'xi', 'xj', 'xk', 'xl', 'xm', 'xn', 'xo', 'xp', 'xq', 'xr', 'xs', 'xt', 'xu', 'xv', 'xw', 'xx', 'xy', 'xz', 'y-', 'y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'yA', 'yB', 'yC', 'yD', 'yE', 'yF', 'yG', 'yH', 'yI', 'yJ', 'yK', 'yL', 'yM', 'yN', 'yO', 'yP', 'yQ', 'yR', 'yS', 'yT', 'yU', 'yV', 'yW', 'yX', 'yY', 'yZ', 'y_', 'ya', 'yb', 'yc', 'yd', 'ye', 'yf', 'yg', 'yh', 'yi', 'yj', 'yk', 'yl', 'ym', 'yn', 'yo', 'yp', 'yq', 'yr', 'ys', 'yt', 'yu', 'yv', 'yw', 'yx', 'yy', 'yz', 'z-', 'z0', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z8', 'z9', 'zA', 'zB', 'zC', 'zD', 'zE', 'zF', 'zG', 'zH', 'zI', 'zJ', 'zK', 'zL', 'zM', 'zN', 'zO', 'zP', 'zQ', 'zR', 'zS', 'zT', 'zU', 'zV', 'zW', 'zX', 'zY', 'zZ', 'z_', 'za', 'zb', 'zc', 'zd', 'ze', 'zf', 'zg', 'zh', 'zi', 'zj', 'zk', 'zl', 'zm', 'zn', 'zo', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zw', 'zx', 'zy', 'zz']

desindex = 0
for item in currentlists:
    if todoitems.index(item) >= desindex:
        desindex = todoitems.index(item) + 1

if desindex >= 4096:
    heroku3.from_key(environ['heroku-key']).apps()[environ['heroku-app']].scale_formation_process('worker', 0)
else:
    heroku3.from_key(environ['heroku-key']).apps()[environ['heroku-app']].config()["url"] = "https://archive.org/download/youtubeannotations_"+str(CHARS_SAFE.index(todoitems[desindex][0])).zfill(2)+"/"+todoitems[desindex]+".tar"

sleep(1)
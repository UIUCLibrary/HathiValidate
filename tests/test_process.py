import os
from unittest.mock import Mock, MagicMock, mock_open, patch

import pytest
import shutil
from hathi_validate import process

dummy_checksum = """693b588c859be9fa1a62f371882e769b *00000001.tif
78036918331dc34fc373bd6f70dbdb91 *00000001.txt
eaa6e3609b941fb5780231e8bd3de4a1 *00000002.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000002.txt
1638aec398bb3b06ec8a26d5737ff5e6 *00000003.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000003.txt
64d96c0eed32acdb617a25e3eb383a60 *00000004.tif
61422a3bee4a9b640275bce101782fe1 *00000004.txt
e6b68dd116cd24b618195c07d9da3f5e *00000005.tif
2abfacb074c11a4217c067a95139fa2f *00000005.txt
55ea66b606b10c26ab934a5807c1c07e *00000006.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000006.txt
6c7b0b5ded74613cdcaa75d3a8455d4b *00000007.tif
99a66eac8c21d0b1bfb8128fad3c7427 *00000007.txt
183f0590d08aa36dddd1bb190b994795 *00000008.tif
1f67e59efa3f9a4b15262273e957bf79 *00000008.txt
c513b5b83afaef3c856ea5edf51546d1 *00000009.tif
82495f97ba86e2cddb8caf7a40cbd18c *00000009.txt
30c67917d26dd07381e79e5b3051f33b *00000010.tif
fab33fa2d6227106c372557f16a5ca5c *00000010.txt
98cb89d7a4d3afca7aa73b68c80902a9 *00000011.tif
63dabccb910f7c7740a5966472ba7a93 *00000011.txt
e7c5424fa27ec3a582162d8e89cba05b *00000012.tif
b23c8718b1ed2c725f78fc73c4d7afa2 *00000012.txt
976f42a40a144579986950805846e446 *00000013.tif
051a3a9ec39d3ad829b5b158e0570d34 *00000013.txt
1e4c331fec42038cffc3984ebcc577d3 *00000014.tif
6f57a24375d6a0444e002c00512216eb *00000014.txt
bcc28f4ebdf36bf4462993d887934064 *00000015.tif
a0d6305df17ba49b19f789b59303715e *00000015.txt
57182108499a947a90725e836df321b5 *00000016.tif
94e41dfb18429eb7ce8a0dd3952a3ffe *00000016.txt
ea946d42800b69479ab68a18d186d2b6 *00000017.tif
b7c46bbb54e9e573b02d668bb24c03d5 *00000017.txt
cea3df2bb2077d79d8aea593cba6ea18 *00000018.tif
9a9968658132c74984b269d9e5886e66 *00000018.txt
c97eed5fdd4007c12230ff1992636ba7 *00000019.tif
e9ac43c7d21b9e44c09e3b8f24070b90 *00000019.txt
e59738f4e8e8f7dbe357450e7e7d5c30 *00000020.tif
1ce49d486e1ba0f09a763e707fccf3ab *00000020.txt
ca3708c6ee11119b9dd39979e1a8488e *00000021.tif
26cd515aa2f29bdfa99838d9b4a2bd4d *00000021.txt
8e892ce05a3c8a13f1c14d30971bad4d *00000022.tif
35205a0f8ca97fc62342b7bdc7a5b351 *00000022.txt
a7aa5253fa30cbff85d966e423d7fc4c *00000023.tif
2e54c6fb5ebb076a64c82c5ec795de51 *00000023.txt
2f11449af46441401d8c28a0fdad810b *00000024.tif
9f409d8c37d21734ead4803411eef45d *00000024.txt
f90aabe1b08a7ea8a6de8815bed5b74c *00000025.tif
b5a520aef967ba4d384e2a513e671571 *00000025.txt
4a67b8ca0cc9e39582f2b88699db9f5b *00000026.tif
7e7dac20195997f17bdacbe31f4f55a6 *00000026.txt
d3a0cde49b02a949f8a5ad7fb457e8b4 *00000027.tif
577203fb28fbe2be2039b345859ba1fb *00000027.txt
05495af90be63312aa11577d4e8545a1 *00000028.tif
97e790761825cc32be7bd93f557a28b3 *00000028.txt
1466633011bf8bd51fb92aac3967f064 *00000029.tif
0be9942b53d81f52af425d6cdd0914a2 *00000029.txt
7ce878233a535992c0d165bbff5b6516 *00000030.tif
c65384ea88c16c216a7da1815fd14b0e *00000030.txt
5faccc3c18a6e864499b434907d06089 *00000031.tif
8c75505a371a7d602475080aa3ca237c *00000031.txt
87a04bb2e264786f904f16f3999a2d50 *00000032.tif
fcd97ea4345fc076d9239a2c3c496bb7 *00000032.txt
b3262a55ab46f6f72a0040f0422bf0fc *00000033.tif
8e735275098522c797e9c253ada68917 *00000033.txt
9b9f686c4aff137a16a4dc639ef8b5b5 *00000034.tif
904b97588d4acdb4570b65d250b0bb9c *00000034.txt
8f0d40b19ec8c0dfe1adc507bfd2b36b *00000035.tif
45a2b59718d07e490628492f8e111236 *00000035.txt
050955076ad7ac55c6e74e1d4b13756a *00000036.tif
d5ae1fc26d6222905cd1f460e1942b4d *00000036.txt
f7ae1e4c142eba96edad226f45e0cafc *00000037.tif
46af36cae5d0c8a791c3e53195e4d1de *00000037.txt
3eef4dfa0647fe62d0df8c8bfa5087a4 *00000038.tif
462ed1b2fe4a0e7ec59a881c0c031313 *00000038.txt
7e12262471b442bb9679d6398b824f7d *00000039.tif
e23deed194ac5d32af08812f3894fdf6 *00000039.txt
cee968f1cc3c1e287ad48b43ab088e63 *00000040.tif
e8b06d36605af00c2102e3646e0b7875 *00000040.txt
45696bafd20fcaf4eb09677f264c3106 *00000041.tif
e999736993130bf30f51d2d888bb709f *00000041.txt
54dd8b35184368a42da095105957ddc0 *00000042.tif
5f06b65cfae45ac1e4f0e8641f09c565 *00000042.txt
4f6b573662a388907a9b6bdd42651432 *00000043.tif
a4f699487d178eef8d638897aa915587 *00000043.txt
2bfc381eab541c9367d8f47ae98a9e04 *00000044.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000044.txt
61d005c4c34772f5d57566e6ca5f6a8e *00000045.tif
152de0dfefaa475ffca1d2ac34c0a45d *00000045.txt
ce7921364b134ec3f116e3de6e565bae *00000046.tif
a05edc2901111f061fb1f22f6f25d008 *00000046.txt
89aa2111f0f688e8d20483b5b1c15f55 *00000047.tif
ac534085bea5ff891e77d6243ed9d711 *00000047.txt
40c210eb70c01c2cfa180b0e5354a5e7 *00000048.tif
1fab868abef43cb8d693f5e9e7373860 *00000048.txt
b118cbc9acc9561501a4e7325484ca49 *00000049.tif
e61e471d58d1cf70b72896f6530e4b90 *00000049.txt
c001760cbf82fab37b207b9530576c78 *00000050.tif
ce5bd2377907d88884ff41fd91bdd6cf *00000050.txt
e063c704b6e00ae0cf215ffff1e7c11c *00000051.tif
695dff352215dcaf8462faa961ac011f *00000051.txt
80a109fcd7b58febe2882040b731507f *00000052.tif
db349f19a30f8b1b17d7f302095a9097 *00000052.txt
7238bb0c275bc9e348c13f89e16f4e39 *00000053.tif
bb044c90551510a3298f7beb2b127f6a *00000053.txt
636aca30107bf4d839118c32474846de *00000054.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000054.txt
64644ddc3226fc8ef62f3a636eba25e6 *00000055.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000055.txt
e6dc59c59f7f075b742f7425aaeeea05 *00000056.tif
ecaa88f7fa0bf610a5a26cf545dcd3aa *00000056.txt
0538bb97e79b4168a726c29db3853ac3 *marc.xml
b7bfccd51c8eed646d767aac9246720b *meta.yml

"""

dummy_marc = """<record xmlns="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
  <leader>01010cam a2200229Ia 4500</leader>
  <controlfield tag="001">7215682</controlfield>
  <controlfield tag="005">20140506141722.0</controlfield>
  <controlfield tag="008">130425s1859    it            000 p ita d</controlfield>
  <datafield ind1=" " ind2=" " tag="035">
    <subfield code="a">(OCoLC)ocn840837733</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="040">
    <subfield code="a">UIU</subfield>
    <subfield code="b">eng</subfield>
    <subfield code="e">dcrmb</subfield>
    <subfield code="c">UIU</subfield>
    <subfield code="d">UIU</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="049">
    <subfield code="a">UIUU</subfield>
    <subfield code="o">skip</subfield>
  </datafield>
  <datafield ind1="1" ind2=" " tag="100">
    <subfield code="a">Carcano, Giulio,</subfield>
    <subfield code="d">1812-1884.</subfield>
  </datafield>
  <datafield ind1="1" ind2="3" tag="245">
    <subfield code="a">La morte di re Carlo Alberto :</subfield>
    <subfield code="b">cantico lirico /</subfield>
    <subfield code="c">di Giulio Carcano.</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="260">
    <subfield code="a">Milano :</subfield>
    <subfield code="b">Coi tipi di Luigi di Giacomo Pirola,</subfield>
    <subfield code="c">1859.</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="300">
    <subfield code="a">12 p. ;</subfield>
    <subfield code="c">26 cm.</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="500">
    <subfield code="a">University of Illinois bookplate: "From the library of Conte Antonio Cavagna Sangiuliani di Gualdana Lazelada di Bereguardo, purchased 1921".</subfield>
    <subfield code="5">IU-R</subfield>
  </datafield>
  <datafield ind1="0" ind2="0" tag="600">
    <subfield code="a">Charles Albert,</subfield>
    <subfield code="c">King of Sardinia,</subfield>
    <subfield code="d">1798-1849</subfield>
    <subfield code="v">Poetry.</subfield>
  </datafield>
  <datafield ind1=" " ind2="7" tag="655">
    <subfield code="a">Occasional poems</subfield>
    <subfield code="z">Italy</subfield>
    <subfield code="y">19th century.</subfield>
    <subfield code="2">rbgenr</subfield>
  </datafield>
  <datafield ind1="1" ind2=" " tag="700">
    <subfield code="a">Cavagna Sangiuliani di Gualdana, Antonio,</subfield>
    <subfield code="c">conte,</subfield>
    <subfield code="d">1843-1913,</subfield>
    <subfield code="e">former owner.</subfield>
    <subfield code="5">IU-R</subfield>
  </datafield>
  <datafield ind1="2" ind2=" " tag="710">
    <subfield code="a">Cavagna Collection (University of Illinois at Urbana-Champaign Library)</subfield>
    <subfield code="5">IU-R</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="752">
    <subfield code="a">Italy</subfield>
    <subfield code="d">Milan.</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="994">
    <subfield code="a">C0</subfield>
    <subfield code="b">UIU</subfield>
  </datafield>
  <datafield ind1=" " ind2=" " tag="955">
    <subfield code="b">7215682</subfield>
  </datafield>
</record>
"""


def checksum_file(tmpdir):
    p = tmpdir.mkdir("tmp").join("checksum.md5")
    p.write(dummy_checksum)
    return p


@pytest.fixture()
def yaml_file_bb(tmpdir_factory):
    base_temp = tmpdir_factory.mktemp("bbyamltest", numbered=False)
    p = base_temp.join("meta.yml")
    with open(str(p), "w") as f:
        f.write("capture_date: 2016-06-21T08:00:00Z\n")
        f.write("capture_agent: TRIGONIX\n")
        f.write("scanner_user: TRIGONIX\n")
        f.write("scanner_make: TRIGONIX\n")
        f.write("scanner_model: TRIGO-C1\n")
    yield str(p)
    shutil.rmtree(base_temp)


def test_bb_yaml(yaml_file_bb):
    errors = process.find_errors_meta(filename=yaml_file_bb, path=os.path.dirname(yaml_file_bb),
                                      require_page_data=False)

    for e in errors:
        print(e.message)
    assert len(errors) == 0


@pytest.fixture()
def ds_with_yml(tmpdir_factory):
    base_temp = tmpdir_factory.mktemp("dsyamltest", numbered=False)
    yaml = base_temp.join("meta.yml")
    with open(str(yaml), "w") as f:
        f.write("capture_date: 2017-07-03T14:22:30-05:00\n")
        f.write("capture_agent: IU\n")
        f.write("scanner_user: University of Illinois Digital Content Creation Unit\n")
        f.write("pagedata:\n")
        f.write("    00000001.jp2: { }\n")
    jp2_file = os.path.join(str(base_temp), "00000001.jp2")
    with open(jp2_file, "wb") as f:
        pass
    yield str(base_temp)
    shutil.rmtree(base_temp)


def test_ds_yaml(ds_with_yml):
    filename = os.path.join(ds_with_yml, "meta.yml")
    errors = process.find_errors_meta(filename=filename, path=ds_with_yml)
    for e in errors:
        print(e.message)
    assert len(errors) == 0


@pytest.fixture()
def marc_file(tmpdir_factory):
    basedir = tmpdir_factory.mktemp("tmp", numbered=False)
    p = basedir.join("marc.xml")
    p.write(dummy_marc)
    yield p
    shutil.rmtree(basedir)


@pytest.mark.skip(reason="not ready yet")
def test_find_failing_checksums(checksum_file):
    print(str(checksum_file))
    process.find_failing_checksums("", str(checksum_file))
    # TODO: FINISH test_find_failing_checksums


def test_parse_checksum():
    md5_hash, file_name = process.parse_checksum("61d005c4c34772f5d57566e6ca5f6a8e *00000045.tif")
    assert md5_hash == "61d005c4c34772f5d57566e6ca5f6a8e"
    assert file_name == "00000045.tif"


def test_parse_checksum_with_two_spaces():
    md5_hash, file_name = process.parse_checksum("D4AB65AE47A6E57194D6847B22DCB14C  00000001.jp2")
    assert md5_hash == "D4AB65AE47A6E57194D6847B22DCB14C"
    assert file_name == "00000001.jp2"


def test_validate_marc(marc_file):
    print("Marc file = {}".format(str(marc_file)))
    errors = list(process.find_errors_marc(str(marc_file)))
    assert errors == []
    pass


class Test_is_same_hash():
    def test_exact_same(self):
        assert process.is_same_hash("D4AB65AE47A6E57194D6847B22DCB14C", "D4AB65AE47A6E57194D6847B22DCB14C") is True

    def test_exact_ignore_case(self):
        assert process.is_same_hash("D4AB65AE47A6E57194D6847B22DCB14C", "d4ab65ae47a6e57194d6847b22dcb14c") is True

    def test_false(self):
        assert process.is_same_hash("D4AB65AE47A6E57194D6847B22DCB14C", "000000000000000000000000000000000") is False

    def test_three_matching(self):
        assert process.is_same_hash(
            "D4AB65AE47A6E57194D6847B22DCB14C",
            "d4ab65ae47a6e57194d6847b22dcb14c",
            "d4ab65ae47a6e57194d6847b22dcb14c") is True

    def test_three_one_missmatch(self):
        assert process.is_same_hash(
            "D4AB65AE47A6E57194D6847B22DCB14C",
            "d4ab65ae47a6e57194d6847b22dcb14c",
            "00000000000000000000000000000000") is False


@pytest.fixture()
def file_with_only_utf8(tmpdir_factory):

    base_temp = tmpdir_factory.mktemp("utf8_tests", numbered=False)
    p = base_temp.join("good.xml")
    UTF_CHAR_LIST = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEF" \
                    "GHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡" \
                    "ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ ¡¢£¤¥¦§¨©ª«¬ ®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈ" \
                    "ÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉ" \
                    "ĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊ" \
                    "ŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſƀƁƂƃƄƅƆƇƈƉƊƋ" \
                    "ƌƍƎƏƐƑƒƓƔƕƖƗƘƙƚƛƜƝƞƟƠơƢƣƤƥƦƧƨƩƪƫƬƭƮƯưƱƲƳƴƵƶƷƸƹƺƻƼƽƾƿǀǁǂǃǄǅǆǇǈǉǊǋǌ" \
                    "ǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǝǞǟǠǡǢǣǤǥǦǧǨǩǪǫǬǭǮǯǰǱǲǳǴǵǶǷǸǹǺǻǼǽǾǿȀȁȂȃȄȅȆȇȈȉȊȋȌȍ" \
                    "ȎȏȐȑȒȓȔȕȖȗȘșȚțȜȝȞȟȠȡȢȣȤȥȦȧȨȩȪȫȬȭȮȯȰȱȲȳȴȵȶȷȸȹȺȻȼȽȾȿɀɁɂɃɄɅɆɇɈɉɊɋɌɍɎ" \
                    "ɏɐɑɒɓɔɕɖɗɘəɚɛɜɝɞɟɠɡɢɣɤɥɦɧɨɩɪɫɬɭɮɯɰɱɲɳɴɵɶɷɸɹɺɻɼɽɾɿʀʁʂʃʄʅʆʇʈʉʊʋʌʍʎʏ" \
                    "ʐʑʒʓʔʕʖʗʘʙʚʛʜʝʞʟʠʡʢʣʤʥʦʧʨʩʪʫʬʭʮʯʰʱʲʳʴʵʶʷʸʹʺʻʼ"

    with open(p, "w", encoding="utf8") as wf:
        for char in UTF_CHAR_LIST:
            wf.write("{}\n".format(char))
    yield p
    shutil.rmtree(base_temp)


def test_utf_check_valid(file_with_only_utf8):
    result = process.find_non_utf8_characters(file_with_only_utf8)
    assert len(result.results) == 0


@pytest.fixture()
def file_with_utf8_and_non_utf8(tmpdir_factory):
    base_temp = tmpdir_factory.mktemp("utf8_tests", numbered=False)
    p = base_temp.join("non_utf8.xml")
    UTF_CHAR_LIST = "abc"
    with open(p, "wb") as wf:

        for char in UTF_CHAR_LIST:
            wf.write(bytes(char, encoding="utf8"))
            wf.write(b"\n")
        wf.write(b'\x80')
    yield p
    shutil.rmtree(base_temp)

def test_utf_check_invalid(file_with_utf8_and_non_utf8):
    result = process.find_non_utf8_characters(file_with_utf8_and_non_utf8)
    assert len(result.results) == 1

def test_find_errors_ocr_valid_no_errors(monkeypatch):
    valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v2#">
    <Description>
        <MeasurementUnit>inch1200</MeasurementUnit>
        <sourceImageInformation>
            <fileName>\\\\libdpsrv1\\storage\\root\\projects\\NDNP\\win_19101017-19101231\\win_19101017-19101231-scan-1-\\ocr\\0070.tif</fileName>
        </sourceImageInformation>
    </Description>
    <Styles></Styles>
    <Layout>
        <Page ID="Dummy" PHYSICAL_IMG_NR="234"></Page>
    </Layout>
</alto>
    """
    mock_path = Mock()

    def mock_scandir(*args, **kwargs):
        mock_xml = MagicMock()
        mock_xml.name = "alto.xml"
        return [
            mock_xml
        ]

    monkeypatch.setattr(os, "scandir", mock_scandir)
    with patch("builtins.open", mock_open(read_data=valid_xml)):
        summary = process.find_errors_ocr(mock_path)
    assert len(summary.results) == 0

def test_find_errors_ocr_invalid_errors(monkeypatch):
    # This missing a Layout element which is a required field
    invalid_xml = """<?xml version="1.0" encoding="UTF-8"?>
<alto xmlns="http://www.loc.gov/standards/alto/ns-v2#">
    <Description>
        <MeasurementUnit>inch1200</MeasurementUnit>
        <sourceImageInformation>
            <fileName>\\\\libdpsrv1\\storage\\root\\projects\\NDNP\\win_19101017-19101231\\win_19101017-19101231-scan-1-\\ocr\\0070.tif</fileName>
        </sourceImageInformation>
    </Description>
    <Styles></Styles>
</alto>
    """
    mock_path = Mock()

    def mock_scandir(_):
        mock_xml = MagicMock()
        mock_xml.name = "alto.xml"
        return [
            mock_xml
        ]

    monkeypatch.setattr(os, "scandir", mock_scandir)
    with patch("builtins.open", mock_open(read_data=invalid_xml)):
        summary = process.find_errors_ocr(mock_path)
    assert len(summary.results) == 1
    assert "does not validate" in summary.results[0].message


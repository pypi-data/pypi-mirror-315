import os
import pytest
from project_paths import paths
from ocfl_rehydration.drs_descriptor import DrsDescriptor
from ocfl_rehydration.drs_file import DrsFile


@pytest.fixture
def descriptor_file_1():
    mets_xml = 'data/16952962/v00001/content/descriptor/46296439_mets.xml'
    return os.path.join(paths.dir_unit_resources, mets_xml)

@pytest.fixture
def descriptor_file_2():
    mets_xml = 'data/27340443/v00001/content/descriptor/2573392_mets.xml'
    return os.path.join(paths.dir_unit_resources, mets_xml)

@pytest.fixture
def expected_1():
    drs_files = {}
    f1 = DrsFile()
    f1.set_id('46296441')
    f1.set_file_name('vzocr2.TXT')
    f1.set_file_dir('ocr_uncorrected')
    drs_files[f1.get_id()] = f1

    f2 = DrsFile()
    f2.set_id('46296442')
    f2.set_file_name('vzocr3.TXT')
    f2.set_file_dir('ocr_uncorrected')
    drs_files[f2.get_id()] = f2

    f3 = DrsFile()
    f3.set_id('46296440')
    f3.set_file_name('vzocr1.txt')
    f3.set_file_dir('ocr_uncorrected')
    drs_files[f3.get_id()] = f3

    return drs_files

@pytest.fixture
def expected_2():
    drs_files = {}
    f1 = DrsFile()
    f1.set_id('1028168')
    f1.set_file_name('_005705781_0001.txt')
    f1.set_file_dir('/')
    f1.set_digest_alg('MD5')
    f1.set_digest_value('bb6df4cc25596c6dd8c6cb9a8060cf40')
    f1.set_mime_type('text/plain')
    drs_files[f1.get_id()] = f1

    f2 = DrsFile()
    f2.set_id('1028170')
    f2.set_file_name('_005705781_0002.txt')
    f2.set_file_dir('/')
    f2.set_digest_alg('MD5')
    f2.set_digest_value('e001ee7dc7134dcda7192486103673d5')
    f2.set_mime_type('text/plain')
    drs_files[f2.get_id()] = f2

    f3 = DrsFile()
    f3.set_id('1028172')
    f3.set_file_name('_005705781_0003.txt')
    f3.set_file_dir('/')
    f3.set_digest_alg('MD5')
    f3.set_digest_value('e9d96ff68f4bb21a65d9206157058f0e')
    f3.set_mime_type('text/plain')
    drs_files[f3.get_id()] = f3

    f4 = DrsFile()
    f4.set_id('1028174')
    f4.set_file_name('_005705781_0004.txt')
    f4.set_file_dir('/')
    f4.set_digest_alg('MD5')
    f4.set_digest_value('4154d62053636345905fcc91dbb9912a')
    f4.set_mime_type('text/plain')
    drs_files[f4.get_id()] = f4

    f5 = DrsFile()
    f5.set_id('1028169')
    f5.set_file_name('_005705781_0002.tif')
    f5.set_file_dir('/')
    f5.set_digest_alg('MD5')
    f5.set_digest_value('9e1cd75876dddc251d2385048bdce23a')
    f5.set_mime_type('image/tiff')
    drs_files[f5.get_id()] = f5

    f6 = DrsFile()
    f6.set_id('1028173')
    f6.set_file_name('_005705781_0004.tif')
    f6.set_file_dir('/')
    f6.set_digest_alg('MD5')
    f6.set_digest_value('16c958906cd869926c5c0f04b24f94c5')
    f6.set_mime_type('image/tiff')
    drs_files[f6.get_id()] = f6

    f7 = DrsFile()
    f7.set_id('1028167')
    f7.set_file_name('_005705781_0001.tif')
    f7.set_file_dir('/')
    f7.set_digest_alg('MD5')
    f7.set_digest_value('4ddc12699510696b7428e31fce489868')
    f7.set_mime_type('image/tiff')
    drs_files[f7.get_id()] = f7

    f8 = DrsFile()
    f8.set_id('1028171')
    f8.set_file_name('_005705781_0003.tif')
    f8.set_file_dir('/')
    f8.set_digest_alg('MD5')
    f8.set_digest_value('d3bc8e8feb3473f97a53cce87a5a1804')
    f8.set_mime_type('image/tiff')
    drs_files[f8.get_id()] = f8

    return drs_files


def test_parse_1(descriptor_file_1, expected_1):
    descriptor = DrsDescriptor(descriptor_file_1)

    # Verify files
    files = descriptor.get_files()
    assert len(files) == len(expected_1)

    for f in files.values():
        expected_file = expected_1.get(f.get_id())
        assert expected_file is not None
        assert f.get_id() == expected_file.get_id()
        assert f.get_file_name() == expected_file.get_file_name()
        assert f.get_file_dir() == expected_file.get_file_dir()
        expected_1.pop(f.get_id())

    assert len(expected_1) == 0


def test_parse_2(descriptor_file_2, expected_2):
    descriptor = DrsDescriptor(descriptor_file_2)

    # Verify files
    files = descriptor.get_files()
    assert len(files) == len(expected_2)

    for f in files.values():        
        expected_file = expected_2.get(f.get_id())
        assert expected_file is not None
        assert f.get_id() == expected_file.get_id()
        assert f.get_file_name() == expected_file.get_file_name()
        assert f.get_file_dir() == expected_file.get_file_dir()
        assert f.get_digest_alg() == expected_file.get_digest_alg()
        assert f.get_digest_value() == expected_file.get_digest_value()
        assert f.get_mime_type() == expected_file.get_mime_type()
        expected_2.pop(f.get_id())

    assert len(expected_2) == 0


def test_get_batch_name():
    descriptor_file_1 = 'data/27997603/v00001/content/descriptor/2573685_mets.xml'
    descriptor_path_1 = os.path.join(paths.dir_unit_resources, descriptor_file_1)
    descriptor_1 = DrsDescriptor(descriptor_path_1)
    assert descriptor_1.get_batch_name() == '1339763.xml'

    descriptor_file_2 = 'data/27340448/v00001/content/descriptor/2573397_mets.xml'
    descriptor_path_2 = os.path.join(paths.dir_unit_resources, descriptor_file_2)
    descriptor_2 = DrsDescriptor(descriptor_path_2)
    assert descriptor_2.get_batch_name() == '1028626.xml'
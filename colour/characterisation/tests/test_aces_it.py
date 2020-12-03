# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour.characterisation.aces_it` module.
"""

import numpy as np
import os
import unittest

from colour.characterisation import (
    MSDS_ACES_RICD, MSDS_CAMERA_SENSITIVITIES, SDS_COLOURCHECKERS,
    sd_to_aces_relative_exposure_values, read_training_data_rawtoaces_v1,
    generate_illuminants_rawtoaces_v1, white_balance_multipliers,
    best_illuminant, normalise_illuminant, training_data_sds_to_RGB,
    training_data_sds_to_XYZ, optimisation_factory_rawtoaces_v1,
    optimisation_factory_JzAzBz, matrix_idt)
from colour.characterisation.aces_it import RESOURCES_DIRECTORY_RAWTOACES
from colour.colorimetry import (MSDS_CMFS, SDS_ILLUMINANTS, SpectralShape,
                                sds_and_msds_to_msds, sd_constant, sd_ones)
from colour.io import read_sds_from_csv_file
from colour.utilities import domain_range_scale

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'MSDS_CANON_EOS_5DMARK_II', 'SD_AMPAS_ISO7589_STUDIO_TUNGSTEN',
    'TestSpectralToAcesRelativeExposureValues',
    'TestReadTrainingDataRawtoacesV1', 'TestGenerateIlluminantsRawtoacesV1',
    'TestWhiteBalanceMultipliers', 'TestBestIlluminant',
    'TestNormaliseIlluminant', 'TestTrainingDataSdsToRGB',
    'TestTrainingDataSdsToXYZ', 'TestOptimizationFactoryRawtoacesV1',
    'TestOptimizationFactoryJzAzBz', 'TestMatrixIdt'
]

MSDS_CANON_EOS_5DMARK_II = sds_and_msds_to_msds(
    read_sds_from_csv_file(
        os.path.join(RESOURCES_DIRECTORY_RAWTOACES,
                     'CANON_EOS_5DMark_II_RGB_Sensitivities.csv')).values())

SD_AMPAS_ISO7589_STUDIO_TUNGSTEN = read_sds_from_csv_file(
    os.path.join(RESOURCES_DIRECTORY_RAWTOACES,
                 'AMPAS_ISO_7589_Tungsten.csv'))['iso7589']


class TestSpectralToAcesRelativeExposureValues(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.\
sd_to_aces_relative_exposure_values` definition unit tests methods.
    """

    def test_spectral_to_aces_relative_exposure_values(self):
        """
        Tests :func:`colour.characterisation.aces_it.
sd_to_aces_relative_exposure_values` definition.
        """

        shape = MSDS_ACES_RICD.shape
        grey_reflector = sd_constant(0.18, shape)
        np.testing.assert_almost_equal(
            sd_to_aces_relative_exposure_values(grey_reflector),
            np.array([0.18, 0.18, 0.18]),
            decimal=7)

        perfect_reflector = sd_ones(shape)
        np.testing.assert_almost_equal(
            sd_to_aces_relative_exposure_values(perfect_reflector),
            np.array([0.97783784, 0.97783784, 0.97783784]),
            decimal=7)

        dark_skin = SDS_COLOURCHECKERS['ColorChecker N Ohta']['dark skin']
        np.testing.assert_almost_equal(
            sd_to_aces_relative_exposure_values(dark_skin),
            np.array([0.11718149, 0.08663609, 0.05897268]),
            decimal=7)

        dark_skin = SDS_COLOURCHECKERS['ColorChecker N Ohta']['dark skin']
        np.testing.assert_almost_equal(
            sd_to_aces_relative_exposure_values(dark_skin,
                                                SDS_ILLUMINANTS['A']),
            np.array([0.13583991, 0.09431845, 0.05928214]),
            decimal=7)

        dark_skin = SDS_COLOURCHECKERS['ColorChecker N Ohta']['dark skin']
        np.testing.assert_almost_equal(
            sd_to_aces_relative_exposure_values(
                dark_skin, apply_chromatic_adaptation=True),
            np.array([0.11807796, 0.08690312, 0.05891252]),
            decimal=7)

        dark_skin = SDS_COLOURCHECKERS['ColorChecker N Ohta']['dark skin']
        np.testing.assert_almost_equal(
            sd_to_aces_relative_exposure_values(
                dark_skin,
                apply_chromatic_adaptation=True,
                chromatic_adaptation_transform='Bradford'),
            np.array([0.11805993, 0.08689013, 0.05900396]),
            decimal=7)

    def test_domain_range_scale_spectral_to_aces_relative_exposure_values(
            self):
        """
        Tests :func:`colour.characterisation.aces_it.
sd_to_aces_relative_exposure_values`  definition domain and range scale
        support.
        """

        shape = MSDS_ACES_RICD.shape
        grey_reflector = sd_constant(0.18, shape)
        RGB = sd_to_aces_relative_exposure_values(grey_reflector)

        d_r = (('reference', 1), (1, 1), (100, 100))
        for scale, factor in d_r:
            with domain_range_scale(scale):
                np.testing.assert_almost_equal(
                    sd_to_aces_relative_exposure_values(grey_reflector),
                    RGB * factor,
                    decimal=7)


class TestReadTrainingDataRawtoacesV1(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.\
read_training_data_rawtoaces_v1` definition unit tests methods.
    """

    def test_read_training_data_rawtoaces_v1(self):
        """
        Tests :func:`colour.characterisation.aces_it.
read_training_data_rawtoaces_v1` definition.
        """

        self.assertEqual(len(read_training_data_rawtoaces_v1().labels), 190)


class TestGenerateIlluminantsRawtoacesV1(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.\
generate_illuminants_rawtoaces_v1` definition unit tests methods.
    """

    def test_generate_illuminants_rawtoaces_v1(self):
        """
        Tests :func:`colour.characterisation.aces_it.
generate_illuminants_rawtoaces_v1` definition.
        """

        self.assertListEqual(
            list(sorted(generate_illuminants_rawtoaces_v1().keys())), [
                '1000K Blackbody', '1500K Blackbody', '2000K Blackbody',
                '2500K Blackbody', '3000K Blackbody', '3500K Blackbody',
                'D100', 'D105', 'D110', 'D115', 'D120', 'D125', 'D130', 'D135',
                'D140', 'D145', 'D150', 'D155', 'D160', 'D165', 'D170', 'D175',
                'D180', 'D185', 'D190', 'D195', 'D200', 'D205', 'D210', 'D215',
                'D220', 'D225', 'D230', 'D235', 'D240', 'D245', 'D250', 'D40',
                'D45', 'D50', 'D55', 'D60', 'D65', 'D70', 'D75', 'D80', 'D85',
                'D90', 'D95', 'iso7589'
            ])


class TestWhiteBalanceMultipliers(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.white_balance_multipliers`
    definition unit tests methods.
    """

    def test_white_balance_multipliers(self):
        """
        Tests :func:`colour.characterisation.aces_it.white_balance_multipliers`
        definition.
        """

        np.testing.assert_almost_equal(
            white_balance_multipliers(MSDS_CANON_EOS_5DMARK_II,
                                      SDS_ILLUMINANTS['D55']),
            np.array([2.34141541, 1.00000000, 1.51633759]),
            decimal=7)

        np.testing.assert_almost_equal(
            white_balance_multipliers(
                MSDS_CANON_EOS_5DMARK_II,
                SDS_ILLUMINANTS['ISO 7589 Studio Tungsten']),
            np.array([1.57095278, 1.00000000, 2.43560477]),
            decimal=7)


class TestBestIlluminant(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.best_illuminant` definition
    unit tests methods.
    """

    def test_best_illuminant(self):
        """
        Tests :func:`colour.characterisation.aces_it.best_illuminant`
        definition.
        """

        self.assertEqual(
            best_illuminant(
                white_balance_multipliers(
                    MSDS_CANON_EOS_5DMARK_II,
                    SDS_ILLUMINANTS['FL2']), MSDS_CANON_EOS_5DMARK_II,
                generate_illuminants_rawtoaces_v1()).name, 'D40')

        self.assertEqual(
            best_illuminant(
                white_balance_multipliers(
                    MSDS_CANON_EOS_5DMARK_II,
                    SDS_ILLUMINANTS['A']), MSDS_CANON_EOS_5DMARK_II,
                generate_illuminants_rawtoaces_v1()).name, '3000K Blackbody')


class TestNormaliseIlluminant(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.normalise_illuminant`
    definition unit tests methods.
    """

    def test_normalise_illuminant(self):
        """
        Tests :func:`colour.characterisation.aces_it.normalise_illuminant`
        definition.
        """

        self.assertAlmostEqual(
            np.sum(
                normalise_illuminant(SDS_ILLUMINANTS['D55'],
                                     MSDS_CANON_EOS_5DMARK_II).values),
            3.439037388220850,
            places=7)


class TestTrainingDataSdsToRGB(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.training_data_sds_to_RGB`
    definition unit tests methods.
    """

    def test_training_data_sds_to_RGB(self):
        """
        Tests :func:`colour.characterisation.aces_it.training_data_sds_to_RGB`
        definition.
        """

        np.testing.assert_almost_equal(
            training_data_sds_to_RGB(read_training_data_rawtoaces_v1(),
                                     MSDS_CANON_EOS_5DMARK_II,
                                     SDS_ILLUMINANTS['D55']),
            np.array([
                [42.00296381, 39.83290349, 43.28842394],
                [181.25453293, 180.47486885, 180.30657630],
                [1580.35041765, 1578.67251435, 1571.05703787],
                [403.67553672, 403.67553672, 403.67553672],
                [1193.51958332, 1194.63985124, 1183.92806238],
                [862.07824054, 863.30644583, 858.29863779],
                [605.42274304, 602.94953701, 596.61414309],
                [395.70687930, 394.67167942, 392.97719777],
                [227.27502116, 228.33554705, 227.96959477],
                [130.97735082, 132.12395139, 131.97239271],
                [61.79308820, 61.85572037, 62.40560537],
                [592.29430914, 383.93309398, 282.70032306],
                [504.67305022, 294.69245978, 193.90976423],
                [640.93167741, 494.91914821, 421.68337308],
                [356.53952646, 239.77610719, 181.18147755],
                [179.58569818, 130.00540238, 109.23999883],
                [1061.07297514, 818.29727750, 730.13362169],
                [765.75936417, 522.06805938, 456.59355601],
                [104.70554060, 80.35106922, 65.75667232],
                [694.19925422, 161.06849749, 214.20170991],
                [1054.83161580, 709.41713619, 668.10329523],
                [697.35479081, 276.20032105, 275.86226833],
                [183.26315174, 65.93801513, 74.60775905],
                [359.74416854, 59.73576149, 89.81296522],
                [1043.53760601, 405.48081521, 376.37298474],
                [344.35374209, 111.26727966, 109.10587712],
                [215.18064862, 87.41152853, 85.18152727],
                [555.37005673, 134.76016985, 111.54658160],
                [931.71846961, 210.02605133, 150.65312210],
                [211.01186324, 50.73939233, 54.55750662],
                [654.45781665, 132.73694874, 107.20009737],
                [1193.89772859, 625.60766645, 521.51066476],
                [802.65730883, 228.94887565, 178.30864097],
                [149.82853589, 44.31839648, 55.29195048],
                [80.88083928, 33.78936351, 41.73438243],
                [579.50157840, 240.80755019, 188.50864121],
                [537.09280420, 80.41714202, 48.28907694],
                [777.62363031, 205.11587061, 122.43126732],
                [292.65436510, 59.53457252, 44.27126512],
                [511.68625012, 134.76897130, 85.73242441],
                [903.64947615, 462.49015529, 350.74183199],
                [852.95457070, 291.64071698, 151.51871958],
                [1427.59841722, 907.54863477, 724.29520203],
                [527.68979414, 169.76114596, 89.48561902],
                [496.62188809, 317.11827387, 243.77642038],
                [554.39017413, 284.77453644, 181.92376325],
                [310.50669032, 96.25812545, 41.22765558],
                [1246.49891599, 522.05121993, 238.28646123],
                [240.19646249, 118.57745244, 82.68426681],
                [1005.98836135, 355.93514762, 118.60457241],
                [792.31376787, 369.56509398, 143.27388201],
                [459.04590557, 315.46594358, 215.53901098],
                [806.50918893, 352.20277469, 97.69239677],
                [1574.11778922, 1078.61331515, 697.02647383],
                [1015.45155837, 598.98507153, 301.94169280],
                [479.68722930, 242.23619637, 72.60351059],
                [1131.70538515, 628.32510627, 213.67910327],
                [185.86573238, 162.55033903, 137.59385867],
                [1131.77074807, 603.89218698, 153.83160203],
                [638.14148862, 527.18090248, 410.12394346],
                [884.58039320, 655.09236879, 329.23967927],
                [1172.73094356, 840.43080883, 380.90114088],
                [1490.24223350, 1111.18491878, 482.33357611],
                [1054.70234779, 513.29967197, 91.55980977],
                [1532.99674295, 1035.15868150, 253.21942988],
                [662.35328287, 528.52354760, 326.56458987],
                [1769.55456145, 1557.58571488, 1155.79098414],
                [1196.62083017, 1079.28012658, 888.47017893],
                [1578.73591185, 1089.40083172, 314.45691871],
                [252.98204345, 206.56788008, 153.62801631],
                [973.59975800, 714.51185344, 251.12884859],
                [1661.01720988, 1340.46809762, 619.61710815],
                [656.66179353, 566.61547800, 322.22788098],
                [676.69663303, 571.86743785, 249.62031449],
                [1229.28626315, 1020.14702709, 353.11090960],
                [390.76190378, 324.36051944, 119.31108035],
                [1524.10495708, 1366.72397704, 633.03830849],
                [1264.54750712, 1149.12002542, 335.25348483],
                [265.96753330, 260.89397210, 130.78590008],
                [90.15969432, 90.72350914, 55.12008388],
                [298.22463247, 300.48700028, 101.95760063],
                [813.34391710, 820.12623357, 313.17818415],
                [186.96402165, 190.38042094, 104.27515726],
                [230.34939258, 235.91900919, 120.77815429],
                [469.57926615, 472.51064145, 256.40912347],
                [117.81249486, 129.17019984, 69.78861213],
                [133.39581196, 151.50390168, 77.66255652],
                [164.19259747, 172.13159331, 80.92295294],
                [146.12230124, 149.32536508, 87.48300520],
                [201.93215173, 208.89885695, 111.84447436],
                [248.41427850, 282.34047722, 122.55482010],
                [304.35509339, 377.38986207, 118.66130122],
                [381.85533606, 530.40398972, 150.83506876],
                [967.19810669, 1161.33086750, 663.54746741],
                [613.98437237, 865.41677370, 362.92357557],
                [410.21304405, 611.89683658, 284.09389273],
                [279.50447144, 416.01646348, 213.18049093],
                [334.48807624, 487.46571814, 235.49134434],
                [664.04349337, 867.87454943, 549.71146455],
                [311.66934673, 431.38058636, 256.13307806],
                [110.04404638, 203.88196409, 104.63331585],
                [153.35857585, 312.67834716, 149.90942505],
                [273.46344514, 462.41992197, 292.50571823],
                [184.77058437, 267.46361125, 193.71894670],
                [75.79805899, 163.84071881, 95.67465270],
                [461.73803707, 668.68797906, 484.77687282],
                [523.01992144, 790.69326153, 598.73122243],
                [105.89414085, 124.92341127, 113.03925656],
                [279.33299507, 446.45128537, 344.73426977],
                [340.57250119, 381.28610429, 353.83182947],
                [141.00956904, 329.50139051, 228.90179483],
                [117.29728945, 156.88993944, 139.49878229],
                [565.12438106, 696.52297174, 615.88218349],
                [1046.73447319, 1446.22424473, 1277.47338963],
                [133.87404291, 253.25944193, 224.75872956],
                [586.52626500, 1015.43013448, 885.49907251],
                [927.08412116, 1197.93784752, 1140.76612264],
                [81.29463446, 202.46201173, 186.35209411],
                [350.90699453, 788.82959642, 669.10307704],
                [278.88231719, 581.42068355, 526.82554470],
                [642.66176703, 990.64038619, 907.64284280],
                [689.10344984, 942.49383066, 900.33073076],
                [190.62073977, 540.21088595, 523.62573562],
                [322.35685764, 676.02683754, 692.94583013],
                [896.29532467, 1289.90474463, 1311.34615018],
                [204.06785020, 321.83261403, 337.01923114],
                [237.10512554, 549.97044011, 646.06486244],
                [907.26703197, 1252.44260107, 1309.50173432],
                [504.74103065, 728.27088424, 782.27808125],
                [470.91049729, 912.49116456, 1059.41083523],
                [231.75497961, 539.14727494, 732.41647792],
                [624.91135978, 943.51709467, 1086.48492282],
                [104.84186738, 398.05825469, 663.96030581],
                [100.47632953, 226.41423139, 323.51675153],
                [998.19560093, 1168.81108673, 1283.07267859],
                [350.74519746, 457.74100518, 552.52270183],
                [223.19531677, 560.14850077, 855.05346039],
                [66.92044931, 128.18947830, 205.30719728],
                [280.63458798, 518.51069955, 784.38948897],
                [1071.24122457, 1267.16339790, 1467.81704311],
                [271.47257445, 553.57609491, 914.33723598],
                [211.86582477, 295.18643027, 418.51776463],
                [153.86457460, 342.06625645, 649.82579665],
                [179.59188635, 265.25370235, 413.68135787],
                [529.77485058, 737.79030218, 1046.29865466],
                [208.71936449, 421.30392624, 796.71281168],
                [685.50294808, 879.76243717, 1195.00892794],
                [85.02189613, 113.33360860, 171.03209018],
                [72.06980264, 139.42600347, 315.97906141],
                [349.57868286, 426.82308690, 556.49647978],
                [726.50329821, 882.48411184, 1163.20130103],
                [102.62158777, 177.73895468, 467.26740089],
                [208.63097281, 322.84137064, 639.30554347],
                [377.19498209, 456.13180268, 706.44272480],
                [149.91131672, 218.16462984, 455.15510078],
                [556.80606655, 673.96774240, 1020.98785748],
                [172.19546054, 181.38617476, 478.69666973],
                [494.98572332, 534.88874559, 773.75255591],
                [1166.31475206, 1207.81829513, 1411.04368728],
                [324.81131421, 298.91188334, 521.96994638],
                [731.58631467, 725.95113189, 1192.71141630],
                [376.70584074, 352.06184423, 572.37854429],
                [421.32413767, 465.07677606, 910.85999527],
                [155.65680826, 145.82096629, 282.56390371],
                [982.43736509, 991.65710582, 1312.39630323],
                [41.37244888, 33.41882583, 59.48460827],
                [282.61535563, 188.37255834, 441.62967707],
                [182.28936533, 136.29152918, 248.30801310],
                [398.28853814, 281.28601665, 641.78038278],
                [494.34030557, 393.91395210, 664.96627121],
                [579.86630787, 449.57878986, 836.64303806],
                [281.30892711, 142.60663373, 309.93723963],
                [439.97606151, 345.13329865, 425.68615785],
                [887.17712876, 583.53811414, 886.88440975],
                [841.97939219, 617.28846790, 810.67002861],
                [1280.60242984, 1139.62066080, 1255.46929276],
                [336.77846782, 246.82877629, 324.48823631],
                [1070.92080733, 527.41599474, 913.93600561],
                [676.57753460, 329.48235976, 509.56020035],
                [1353.12934453, 1048.28092139, 1227.42851889],
                [248.56120754, 78.30056642, 137.39216268],
                [675.76876164, 381.60749713, 545.08703142],
                [1008.57884369, 704.64042514, 836.94311729],
                [1207.19931876, 527.74482440, 737.30284625],
                [1157.60714894, 736.24734736, 846.01278626],
                [861.62204402, 714.70913295, 747.29294390],
                [255.83324360, 94.08214754, 147.60127564],
                [1522.93390177, 1017.14491217, 1073.23488749],
                [460.59077351, 93.73852735, 210.75844436],
                [909.87331348, 498.83253656, 750.09672276],
            ]),
            decimal=7)

        training_data = sds_and_msds_to_msds(
            SDS_COLOURCHECKERS['BabelColor Average'].values())
        np.testing.assert_almost_equal(
            training_data_sds_to_RGB(training_data, MSDS_CANON_EOS_5DMARK_II,
                                     SDS_ILLUMINANTS['D55']),
            np.array([
                [263.80361607, 170.29412869, 132.71463416],
                [884.07936328, 628.44083126, 520.43504675],
                [324.17856150, 443.95092266, 606.43750890],
                [243.82059773, 253.22111395, 144.98600653],
                [481.54199203, 527.96925768, 764.50624747],
                [628.07015143, 979.73104655, 896.85237907],
                [927.63600544, 391.11468312, 150.73047156],
                [203.13259862, 317.65395368, 639.54581080],
                [686.28955864, 260.78688114, 254.89963998],
                [174.05857536, 132.16684952, 230.54054095],
                [806.50094411, 817.35481419, 312.91902292],
                [1111.20280010, 608.82554576, 194.31984092],
                [94.99792206, 185.04148229, 456.53592437],
                [340.60457483, 498.62910631, 254.08356415],
                [531.53679194, 136.11844274, 109.19876416],
                [1387.37113491, 952.84382040, 286.23152122],
                [681.97933172, 326.66634506, 526.23078660],
                [244.90739217, 554.88866566, 741.21522946],
                [1841.80020583, 1834.49277300, 1784.07500285],
                [1179.76201558, 1189.84138939, 1182.25520674],
                [720.27089899, 726.91855632, 724.84766858],
                [382.16849234, 387.41521539, 386.87510339],
                [178.43859184, 181.76108810, 182.71062184],
                [64.77754952, 64.80020759, 65.45515287],
            ]),
            decimal=7)


class TestTrainingDataSdsToXYZ(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.training_data_sds_to_XYZ`
    definition unit tests methods.
    """

    def test_training_data_sds_to_XYZ(self):
        """
        Tests :func:`colour.characterisation.aces_it.training_data_sds_to_XYZ`
        definition.
        """

        np.testing.assert_almost_equal(
            training_data_sds_to_XYZ(
                read_training_data_rawtoaces_v1(),
                MSDS_CMFS['CIE 1931 2 Degree Standard Observer'],
                SDS_ILLUMINANTS['D55']),
            np.array([
                [0.01743541, 0.01795040, 0.01961110],
                [0.08556071, 0.08957352, 0.09017032],
                [0.74558770, 0.78175495, 0.78343383],
                [0.19005289, 0.19950000, 0.20126062],
                [0.56263167, 0.59145443, 0.58944868],
                [0.40708229, 0.42774653, 0.42813199],
                [0.28533739, 0.29945717, 0.29732644],
                [0.18670375, 0.19575576, 0.19612855],
                [0.10734487, 0.11290543, 0.11381239],
                [0.06188310, 0.06524694, 0.06594260],
                [0.02905436, 0.03045954, 0.03111642],
                [0.25031624, 0.22471846, 0.12599982],
                [0.20848487, 0.18072652, 0.08216289],
                [0.28173081, 0.26937432, 0.19943363],
                [0.15129458, 0.13765872, 0.08086671],
                [0.07854243, 0.07274480, 0.05123870],
                [0.46574583, 0.43948749, 0.34501135],
                [0.33111608, 0.29368033, 0.21379720],
                [0.04596029, 0.04443836, 0.03115443],
                [0.28422646, 0.15495892, 0.11586479],
                [0.47490187, 0.41497780, 0.33505853],
                [0.29452546, 0.20003225, 0.13705453],
                [0.06905269, 0.04421818, 0.03449201],
                [0.13040440, 0.06239791, 0.04175606],
                [0.43838730, 0.29962261, 0.18439668],
                [0.13390118, 0.08356608, 0.04956679],
                [0.08356733, 0.05794634, 0.03910007],
                [0.21637988, 0.12469189, 0.04842559],
                [0.37899204, 0.22130821, 0.07365608],
                [0.07733610, 0.04256869, 0.02300063],
                [0.25696432, 0.14119282, 0.04740500],
                [0.51960474, 0.41409496, 0.25643556],
                [0.32241564, 0.19954021, 0.08051276],
                [0.05811798, 0.03389661, 0.02553745],
                [0.03192572, 0.02139972, 0.01894908],
                [0.24605476, 0.17854962, 0.09147038],
                [0.20624731, 0.10555152, 0.01675508],
                [0.31255107, 0.19334840, 0.05143990],
                [0.11006219, 0.06057155, 0.01700794],
                [0.20509764, 0.12555310, 0.03594860],
                [0.38058683, 0.30396093, 0.16256996],
                [0.34354473, 0.23964048, 0.06111316],
                [0.62251344, 0.54770879, 0.34634977],
                [0.21294652, 0.14470338, 0.03492000],
                [0.22064317, 0.19656587, 0.11907643],
                [0.23955073, 0.19768225, 0.08595970],
                [0.12377361, 0.08353105, 0.01434151],
                [0.52378659, 0.40757502, 0.10242337],
                [0.09732322, 0.07735501, 0.03254246],
                [0.41081884, 0.30127969, 0.04240016],
                [0.32946008, 0.27129095, 0.05232655],
                [0.19870991, 0.18701769, 0.09764509],
                [0.31867743, 0.25717029, 0.02158054],
                [0.67745549, 0.64283785, 0.31268426],
                [0.43182429, 0.39425828, 0.13198410],
                [0.19075096, 0.16573196, 0.01845293],
                [0.47578930, 0.43714747, 0.07974541],
                [0.08420865, 0.08615579, 0.06605406],
                [0.47306132, 0.43488423, 0.05262924],
                [0.28242654, 0.28638349, 0.19186089],
                [0.37367384, 0.38524079, 0.13498637],
                [0.49536547, 0.51027091, 0.15645211],
                [0.63680942, 0.67272132, 0.19642820],
                [0.43790684, 0.39093965, 0.02518505],
                [0.63216527, 0.66425603, 0.07124985],
                [0.28682848, 0.29807036, 0.14308787],
                [0.78666095, 0.83181391, 0.53110094],
                [0.54475049, 0.57280425, 0.43240766],
                [0.65555915, 0.68992930, 0.10030198],
                [0.10560623, 0.10992647, 0.06863885],
                [0.40588908, 0.43345904, 0.08589490],
                [0.69824760, 0.76446843, 0.23843395],
                [0.27951451, 0.30869595, 0.13310650],
                [0.28351930, 0.32278417, 0.09130925],
                [0.51144946, 0.58985649, 0.11409286],
                [0.16769668, 0.19357639, 0.04824163],
                [0.64027510, 0.74864980, 0.24145602],
                [0.51533750, 0.64418491, 0.09390029],
                [0.10903312, 0.13420204, 0.04403235],
                [0.03916991, 0.04755109, 0.02410291],
                [0.12726285, 0.16825903, 0.03705646],
                [0.34079923, 0.44119883, 0.10621489],
                [0.08299513, 0.10226271, 0.04607974],
                [0.10117617, 0.12690940, 0.05211600],
                [0.20673305, 0.25456362, 0.11244267],
                [0.05040081, 0.06702198, 0.02944861],
                [0.05809758, 0.07896803, 0.03312583],
                [0.07202711, 0.09383365, 0.03453490],
                [0.06392748, 0.07896740, 0.03860393],
                [0.08851258, 0.11174080, 0.04873213],
                [0.09821259, 0.13743849, 0.03901353],
                [0.12253000, 0.18989034, 0.03327101],
                [0.15082798, 0.25948217, 0.03805919],
                [0.41476613, 0.56455709, 0.26988900],
                [0.25043710, 0.40869656, 0.12211755],
                [0.17536685, 0.28765326, 0.10166502],
                [0.12038544, 0.19242328, 0.07754636],
                [0.14661345, 0.23524743, 0.09334793],
                [0.29469553, 0.41056592, 0.23093160],
                [0.13015693, 0.19492122, 0.09333495],
                [0.04081181, 0.08280292, 0.03122401],
                [0.06569736, 0.13553353, 0.05266408],
                [0.12177383, 0.20160583, 0.11621774],
                [0.08354206, 0.11970984, 0.08207175],
                [0.02834645, 0.06259404, 0.03135058],
                [0.20884161, 0.29927365, 0.20553553],
                [0.23180119, 0.33870071, 0.24267407],
                [0.04413521, 0.05398934, 0.04862030],
                [0.13068910, 0.19470885, 0.15073584],
                [0.16108644, 0.18484544, 0.17474649],
                [0.06206737, 0.12873462, 0.09368693],
                [0.05126858, 0.06722639, 0.05961970],
                [0.25534374, 0.31335090, 0.27780291],
                [0.48369629, 0.63319069, 0.57347864],
                [0.06066266, 0.09712274, 0.09253437],
                [0.27940216, 0.41909220, 0.39351159],
                [0.44664100, 0.54665344, 0.55342931],
                [0.03590889, 0.06959304, 0.07535965],
                [0.16621092, 0.30339106, 0.29722885],
                [0.12909138, 0.22008859, 0.22690521],
                [0.31015553, 0.42498221, 0.42044232],
                [0.33970423, 0.42779997, 0.43883150],
                [0.10000582, 0.19440825, 0.23393750],
                [0.16694758, 0.26056864, 0.32541934],
                [0.43598087, 0.55484571, 0.63089871],
                [0.10305166, 0.13633951, 0.16650820],
                [0.12725465, 0.19404057, 0.30068226],
                [0.44450660, 0.54666776, 0.64220554],
                [0.25312549, 0.31346831, 0.38485942],
                [0.24557618, 0.34698805, 0.51328941],
                [0.13585660, 0.18761687, 0.36302217],
                [0.32288492, 0.39652004, 0.54579104],
                [0.08400465, 0.11889755, 0.34519851],
                [0.06038029, 0.07936884, 0.16393180],
                [0.47840043, 0.53070661, 0.64043584],
                [0.16727376, 0.19048161, 0.27055547],
                [0.14740952, 0.19227205, 0.44545300],
                [0.03953792, 0.04540593, 0.10766386],
                [0.16200092, 0.18995251, 0.41003367],
                [0.53147895, 0.57554326, 0.74787983],
                [0.17107460, 0.19285623, 0.48157477],
                [0.11394187, 0.12139868, 0.21928748],
                [0.10838799, 0.11193347, 0.34884682],
                [0.10390937, 0.10854555, 0.22459293],
                [0.28493924, 0.30349174, 0.54832107],
                [0.13572090, 0.13988801, 0.43412229],
                [0.36141619, 0.37929776, 0.62919317],
                [0.04527113, 0.04612919, 0.09028801],
                [0.05164102, 0.04505136, 0.17732932],
                [0.18148861, 0.19085005, 0.29528314],
                [0.37792382, 0.39238764, 0.61357669],
                [0.08148672, 0.06054619, 0.27321036],
                [0.13431208, 0.12118937, 0.35762939],
                [0.19932157, 0.19328547, 0.37878896],
                [0.09456787, 0.08094285, 0.25785832],
                [0.29868476, 0.28967149, 0.54786550],
                [0.09582629, 0.06156148, 0.27163852],
                [0.25053785, 0.23630807, 0.40751054],
                [0.56821117, 0.57452018, 0.72419232],
                [0.16116009, 0.13379410, 0.28760107],
                [0.37816205, 0.32564214, 0.64945876],
                [0.19440630, 0.16599850, 0.31684298],
                [0.24229817, 0.19698372, 0.51538353],
                [0.08104904, 0.06295569, 0.15738669],
                [0.48808364, 0.46372832, 0.69336648],
                [0.01983575, 0.01538929, 0.03252398],
                [0.13468770, 0.08473328, 0.25136965],
                [0.08762890, 0.06560340, 0.13804375],
                [0.20192043, 0.12939477, 0.36343630],
                [0.24231283, 0.19018859, 0.36604686],
                [0.28784724, 0.21105155, 0.46114703],
                [0.12549222, 0.07471177, 0.17126268],
                [0.20910983, 0.18235419, 0.22475458],
                [0.43032307, 0.32727171, 0.49574549],
                [0.39105442, 0.32475758, 0.42885925],
                [0.60567491, 0.57928897, 0.64030251],
                [0.15645417, 0.12986348, 0.17171885],
                [0.50025055, 0.32646202, 0.51899239],
                [0.29822363, 0.19839451, 0.27397060],
                [0.63136923, 0.55375993, 0.63816664],
                [0.10261977, 0.05754107, 0.07473368],
                [0.30325538, 0.21976283, 0.29171854],
                [0.46794841, 0.39368920, 0.44286306],
                [0.54326558, 0.36319029, 0.41127862],
                [0.52355493, 0.42261205, 0.43529051],
                [0.39852212, 0.37568122, 0.37825751],
                [0.10892106, 0.06698290, 0.07939788],
                [0.68780223, 0.58022018, 0.54422258],
                [0.18984448, 0.09051898, 0.12104133],
                [0.41991006, 0.29457037, 0.40780639],
            ]),
            decimal=7)

        training_data = sds_and_msds_to_msds(
            SDS_COLOURCHECKERS['BabelColor Average'].values())

        np.testing.assert_almost_equal(
            training_data_sds_to_XYZ(
                training_data,
                MSDS_CMFS['CIE 1931 2 Degree Standard Observer'],
                SDS_ILLUMINANTS['D55']),
            np.array([
                [0.11386016, 0.10184316, 0.06318332],
                [0.38043230, 0.34842093, 0.23582246],
                [0.17359019, 0.18707491, 0.31848244],
                [0.10647823, 0.13300376, 0.06486355],
                [0.24658643, 0.23417740, 0.40546447],
                [0.30550003, 0.42171110, 0.41928361],
                [0.38409200, 0.30325611, 0.05955461],
                [0.13149767, 0.11720378, 0.35673016],
                [0.28717811, 0.19215580, 0.12514286],
                [0.08401031, 0.06423349, 0.12782115],
                [0.33990604, 0.44124555, 0.10834694],
                [0.46443889, 0.42686462, 0.07340585],
                [0.07650085, 0.06051409, 0.26167301],
                [0.14598990, 0.23185071, 0.09380297],
                [0.20642710, 0.12162691, 0.04673088],
                [0.57371755, 0.59896814, 0.08930486],
                [0.30208819, 0.19714705, 0.28492050],
                [0.14184323, 0.19554336, 0.36653731],
                [0.86547610, 0.91241348, 0.88583082],
                [0.55802432, 0.58852191, 0.59042758],
                [0.34102067, 0.35951875, 0.36251375],
                [0.18104441, 0.19123509, 0.19353380],
                [0.08461047, 0.08944605, 0.09150081],
                [0.03058273, 0.03200953, 0.03277947],
            ]),
            decimal=7)


class TestOptimizationFactoryRawtoacesV1(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.\
optimisation_factory_rawtoaces_v1` definition unit tests methods.
    """

    def test_optimisation_factory_rawtoaces_v1(self):
        """
        Tests :func:`colour.characterisation.aces_it.\
optimisation_factory_rawtoaces_v1` definition.
        """

        self.assertEqual(len(optimisation_factory_rawtoaces_v1()), 2)


class TestOptimizationFactoryJzAzBz(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.\
optimisation_factory_JzAzBz` definition unit tests methods.
    """

    def test_optimisation_factory_JzAzBz(self):
        """
        Tests :func:`colour.characterisation.aces_it.\
optimisation_factory_JzAzBz` definition.
        """

        self.assertEqual(len(optimisation_factory_JzAzBz()), 2)


class TestMatrixIdt(unittest.TestCase):
    """
    Defines :func:`colour.characterisation.aces_it.matrix_idt`
    definition unit tests methods.
    """

    def test_matrix_idt(self):
        """
        Tests :func:`colour.characterisation.aces_it.matrix_idt`
        definition.
        """

        # The *RAW to ACES* v1 matrix for the same camera and optimized by
        # `Ceres Solver <http://ceres-solver.org/>`__ is as follows:
        #
        # 0.864994 -0.026302 0.161308
        # 0.056527 1.122997 -0.179524
        # 0.023683 -0.202547 1.178864
        np.testing.assert_allclose(
            matrix_idt(MSDS_CANON_EOS_5DMARK_II, SDS_ILLUMINANTS['D55']),
            np.array([
                [0.84993207, -0.01605594, 0.15143504],
                [0.05090392, 1.12559930, -0.18498249],
                [0.02006825, -0.19445149, 1.16206549],
            ]),
            rtol=0.0001,
            atol=0.0001)

        # The *RAW to ACES* v1 matrix for the same camera and optimized by
        # `Ceres Solver <http://ceres-solver.org/>`__ is as follows:
        #
        # 0.888492 -0.077505 0.189014
        # 0.021805 1.066614 -0.088418
        # -0.019718 -0.206664 1.226381
        np.testing.assert_allclose(
            matrix_idt(MSDS_CANON_EOS_5DMARK_II,
                       SD_AMPAS_ISO7589_STUDIO_TUNGSTEN),
            np.array([
                [0.85895300, -0.04381920, 0.15978620],
                [0.01024800, 1.08825364, -0.11392229],
                [-0.02327674, -0.18044292, 1.15903609],
            ]),
            rtol=0.0001,
            atol=0.0001)

        np.testing.assert_allclose(
            matrix_idt(
                MSDS_CANON_EOS_5DMARK_II,
                SDS_ILLUMINANTS['D55'],
                optimisation_factory=optimisation_factory_JzAzBz),
            np.array([
                [0.84841492, -0.01569765, 0.15799332],
                [0.05333075, 1.11428542, -0.17523500],
                [0.02262287, -0.22527728, 1.19646895],
            ]),
            rtol=0.0001,
            atol=0.0001)

        np.testing.assert_allclose(
            matrix_idt(
                MSDS_CANON_EOS_5DMARK_II,
                SDS_ILLUMINANTS['D55'],
                optimisation_kwargs={'method': 'Nelder-Mead'}),
            np.array([
                [0.71327381, 0.19213397, 0.11115511],
                [-0.05788252, 1.31165598, -0.21730625],
                [-0.05913103, -0.02787107, 1.10737947],
            ]),
            rtol=0.0001,
            atol=0.0001)

        training_data = sds_and_msds_to_msds(
            SDS_COLOURCHECKERS['BabelColor Average'].values())

        np.testing.assert_allclose(
            matrix_idt(
                MSDS_CAMERA_SENSITIVITIES['Nikon 5100 (NPL)'].copy().align(
                    SpectralShape(400, 700, 10)),
                SD_AMPAS_ISO7589_STUDIO_TUNGSTEN,
                training_data=training_data),
            np.array([
                [0.74041064, 0.10951105, 0.11963256],
                [-0.00467360, 1.09238438, -0.11398966],
                [0.06728533, -0.29530438, 1.18589793],
            ]),
            rtol=0.0001,
            atol=0.0001)


if __name__ == '__main__':
    unittest.main()

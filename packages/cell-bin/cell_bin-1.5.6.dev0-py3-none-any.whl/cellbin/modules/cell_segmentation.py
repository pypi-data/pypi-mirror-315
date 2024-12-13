from cellbin.modules import CellBinElement
from cellbin.dnn.cseg.detector import Segmentation
from cellbin.dnn.cseg.cell_trace import get_trace as get_t
from cellbin.dnn.cseg.cell_trace import get_trace_v2 as get_t_v2
from cellbin.utils import clog
from cellbin.modules import StainType

SUPPORTED_TYPES = [StainType.ssDNA.value, StainType.HE.value, StainType.DAPI.value, StainType.rna.value]


class CellSegmentation(CellBinElement):
    def __init__(
            self,
            model_path,
            gpu="-1",
            num_threads=0,
            img_type=''
    ):
        """
        Args:
            model_path(str): network model file path
            gpu(str): gpu index
            num_threads(int): default is 0,When you use the CPU,
            you can use it to control the maximum number of threads
        """
        super(CellSegmentation, self).__init__()

        self._MODE = "onnx"
        self._NET = "bcdu"
        self.img_type = img_type
        if self.img_type.upper() not in SUPPORTED_TYPES:
            clog.warning(f"{self.img_type.upper()} not in supported list {SUPPORTED_TYPES}, use default "
                         f"{StainType.ssDNA.value}")
            self.img_type = StainType.ssDNA.value
        if self.img_type.upper() == StainType.rna.value:
            self._WIN_SIZE = (512, 512)
            self._INPUT_SIZE = (1, 512, 512)
            self._OVERLAP = 0.1
        else:
            self._WIN_SIZE = (256, 256)
            self._INPUT_SIZE = (256, 256, 1)
            self._OVERLAP = 16

        self._gpu = gpu
        self._model_path = model_path
        self._num_threads = num_threads

        self._cell_seg = Segmentation(
            net=self._NET,
            mode=self._MODE,
            gpu=self._gpu,
            num_threads=self._num_threads,
            win_size=self._WIN_SIZE,
            intput_size=self._INPUT_SIZE,
            overlap=self._OVERLAP,
            img_type=self.img_type
        )
        clog.info("start loading model weight")
        self._cell_seg.f_init_model(model_path=self._model_path)
        clog.info("end loading model weight")

    def run(self, img):
        """
        run cell predict
        Args:
            img(ndarray): img array

        Returns(ndarray):cell mask

        """
        clog.info("start cell segmentation")
        mask = self._cell_seg.f_predict(img)
        clog.info("end cell segmentation")
        return mask

    @staticmethod
    def get_trace(mask):
        """
        2023/09/20 @fxzhao 对大尺寸图片采用加速版本以降低内存
        """
        if mask.shape[0] > 40000:
            return get_t_v2(mask)
        else:
            return get_t(mask)

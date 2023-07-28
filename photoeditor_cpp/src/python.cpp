#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include <photoeditor_cpp/test.hpp>
#include <opencv2/opencv.hpp>

namespace py = pybind11;

template <typename T>
auto get_cv_type(){
    if constexpr (std::is_same_v<T,uint8_t>){
        return CV_8U;
    }
    if constexpr (std::is_same_v<T,int8_t>){
        return CV_8S;
    }
    if constexpr (std::is_same_v<T,uint16_t>){
        return CV_16U;
    }
    if constexpr (std::is_same_v<T,int16_t>){
        return CV_16S;
    }
    if constexpr (std::is_same_v<T,int32_t>){
        return CV_32S;
    }
    if constexpr (std::is_same_v<T,float>){
        return CV_32F;
    }
    if constexpr (std::is_same_v<T,double>){
        return CV_64F;
    }
    throw std::runtime_error("Invalid numpy array as cv::Mat");
}

template<typename T>
cv::Mat cv_from_numpy(py::array_t<T>& img)
{   
    auto cv_type = get_cv_type<T>();
    return {img.shape(0), img.shape(1), CV_MAKETYPE(cv_type, img.shape(2)),
                const_cast<T*>(img.data()), img.strides(0)};
}
template cv::Mat cv_from_numpy(py::array_t<uint8_t>& img);
template cv::Mat cv_from_numpy(py::array_t<int8_t>& img);
template cv::Mat cv_from_numpy(py::array_t<uint16_t>& img);
template cv::Mat cv_from_numpy(py::array_t<int16_t>& img);
template cv::Mat cv_from_numpy(py::array_t<int32_t>& img);
template cv::Mat cv_from_numpy(py::array_t<float>& img);
template cv::Mat cv_from_numpy(py::array_t<double>& img);


std::map<int,std::string> depth_to_dtype={
    { CV_8U,  py::format_descriptor<uint8_t>::format() },
    { CV_8S,  py::format_descriptor<int8_t>::format() },
    { CV_16U, py::format_descriptor<uint16_t>::format() },
    { CV_16S, py::format_descriptor<int16_t>::format() },
    { CV_32S, py::format_descriptor<int32_t>::format() },
    { CV_32F, py::format_descriptor<float>::format()},
    { CV_64F, py::format_descriptor<double>::format() },
};
py::dtype determine_np_dtype(int cv_depth)
{
    return py::dtype(depth_to_dtype[cv_depth]);
}

py::capsule make_capsule(const cv::Mat& m)
{
    return py::capsule(new cv::Mat(m)
        , [](void *v) { delete reinterpret_cast<cv::Mat*>(v); }
        );
}

py::array cv_to_numpy(const cv::Mat& mat){
    return {
        determine_np_dtype(mat.depth()),
        {mat.rows,mat.cols,mat.channels()},
        mat.data,
        make_capsule(mat)
    };
}


PYBIND11_MODULE(photoeditor_cpp, m) {
    m.doc() = R"pbdoc(
        Photoeditor cpp library plugin
        -----------------------

        .. currentmodule:: photoeditor_cpp

        .. autosummary::
           :toctree: _generate

    )pbdoc";

    m.def("show", [](py::array_t<uint8_t>& img) {phe::show(cv_from_numpy(img));});
    m.def("show", [](py::array_t<int8_t>& img)  {phe::show(cv_from_numpy(img));});
    m.def("show", [](py::array_t<uint16_t>& img){phe::show(cv_from_numpy(img));});
    m.def("show", [](py::array_t<int16_t>& img) {phe::show(cv_from_numpy(img));});
    m.def("show", [](py::array_t<int32_t>& img) {phe::show(cv_from_numpy(img));});
    m.def("show", [](py::array_t<float>& img)   {phe::show(cv_from_numpy(img));});
    m.def("show", [](py::array_t<double>& img)  {phe::show(cv_from_numpy(img));});


    m.def("identity", [](py::array_t<uint8_t>& img) {return cv_to_numpy(phe::identity(cv_from_numpy(img)));});
    m.def("identity", [](py::array_t<int8_t>& img)  {return cv_to_numpy(phe::identity(cv_from_numpy(img)));});
    m.def("identity", [](py::array_t<uint16_t>& img){return cv_to_numpy(phe::identity(cv_from_numpy(img)));});
    m.def("identity", [](py::array_t<int16_t>& img) {return cv_to_numpy(phe::identity(cv_from_numpy(img)));});
    m.def("identity", [](py::array_t<int32_t>& img) {return cv_to_numpy(phe::identity(cv_from_numpy(img)));});
    m.def("identity", [](py::array_t<float>& img)   {return cv_to_numpy(phe::identity(cv_from_numpy(img)));});
    m.def("identity", [](py::array_t<double>& img)  {return cv_to_numpy(phe::identity(cv_from_numpy(img)));});


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
if(USE_RANDOM)
  message(STATUS "Build with contrib.random")
  file(GLOB RANDOM_CONTRIB_SRC src/contrib/random/random.cc)
  list(APPEND RUNTIME_SRCS ${RANDOM_CONTRIB_SRC})
endif(USE_RANDOM)
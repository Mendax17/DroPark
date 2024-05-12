// Generated by gencpp from file morai_msgs/MultiPlayEventRequest.msg
// DO NOT EDIT!


#ifndef MORAI_MSGS_MESSAGE_MULTIPLAYEVENTREQUEST_H
#define MORAI_MSGS_MESSAGE_MULTIPLAYEVENTREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace morai_msgs
{
template <class ContainerAllocator>
struct MultiPlayEventRequest_
{
  typedef MultiPlayEventRequest_<ContainerAllocator> Type;

  MultiPlayEventRequest_()
    : requestRespawn(false)  {
    }
  MultiPlayEventRequest_(const ContainerAllocator& _alloc)
    : requestRespawn(false)  {
  (void)_alloc;
    }



   typedef uint8_t _requestRespawn_type;
  _requestRespawn_type requestRespawn;





  typedef boost::shared_ptr< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> const> ConstPtr;

}; // struct MultiPlayEventRequest_

typedef ::morai_msgs::MultiPlayEventRequest_<std::allocator<void> > MultiPlayEventRequest;

typedef boost::shared_ptr< ::morai_msgs::MultiPlayEventRequest > MultiPlayEventRequestPtr;
typedef boost::shared_ptr< ::morai_msgs::MultiPlayEventRequest const> MultiPlayEventRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator1> & lhs, const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator2> & rhs)
{
  return lhs.requestRespawn == rhs.requestRespawn;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator1> & lhs, const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace morai_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "6d7b6e13e2c1671b06638e7f201595a3";
  }

  static const char* value(const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x6d7b6e13e2c1671bULL;
  static const uint64_t static_value2 = 0x06638e7f201595a3ULL;
};

template<class ContainerAllocator>
struct DataType< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "morai_msgs/MultiPlayEventRequest";
  }

  static const char* value(const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bool requestRespawn\n"
;
  }

  static const char* value(const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.requestRespawn);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MultiPlayEventRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::morai_msgs::MultiPlayEventRequest_<ContainerAllocator>& v)
  {
    s << indent << "requestRespawn: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.requestRespawn);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MORAI_MSGS_MESSAGE_MULTIPLAYEVENTREQUEST_H
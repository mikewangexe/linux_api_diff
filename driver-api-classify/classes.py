class_dict = {}
class_order = [     'Misc',
                    'Framework/DRM',
                    'Framework/Network',
                    'Framework/Generic',
                    'Framework/Ethernet',
                    'Framework/kobject',
                    'Framework/Input',
                    'Framework/Backlight',
                    'Framework/hwmon',
                    'Framework/MTD',
                    'Framework/MFD',
                    'Framework/tty',
                    'Framework/Block',
                    'Framework/Sound',
                    'Framework/Char',
                    'Sync/sema',
                    'Sync/lock',
                    'IOMMU',
                    'Memory/net',
                    'Memory/vmalloc',
                    'Memory/kmalloc',
                    'Memory',
                    'Bus/PCI',
                    'Bus/ATA',
                    'Bus/Platform',
                    'Bus/I2C',
                    'Bus/SCSI',
                    'Bus/USB',
                    'Bus/SPI',
                    'Bus/Parallel-Port',
                    'Bus/Parallel-Port-IDE',
                    'Bus/PCMCIA',
                    'Module',
                    'Klib',
                    'Klib/fs',
                    'Security',
                    'Deferred-Work',
                    'Cross-Module-Call',
                    'DMA',
                    'Resource-Manage',
                    'Sync/atomic',
                    'Sync/completion',
                    'Sync/rcu',
                    'Sched',
                    'Time',
                    'Interrupt',
                    'Framebuffer',
                    'Platform',
                    'Delay',
                    'Delay/timer',
                    'Delay/workqueue',
                    'Delay/waitqueue',
                    'Delay/tasklet',
                    'Fs/vfs',
                    'ACPI',
                    'Xen-specific',
                    'Firmware',
                    'GPIO-Pin-Controller',
                    'Debugger',
                    'Randomness',
                    'HDMI',
                    'Signal',
                    'QoS-Manage',
                    'CDROM',
                    'Power/CPU-Freq',
                    'Power/Voltage-Current-Regulator',
                    'Power/Manage',
                    'EFI',
                    'Async-Calls',
                    'Multi-core Support',
                    'IO-Primitives',
                    'drv/net/e1000',
                    'Project'
        ]
class_dict['Module'] = {    'path' : [],
                            'file' : ['module.', 'moduleparam', 'kmod'],
                            'exc' : [],
                            'func' : ['module']
        }
class_dict['Misc'] = { 'path' : [], 
                            'exc' : [],
                                'file' : [], 
                                'func' : [] 
                              }
class_dict['Framework/DRM'] = { 'path' : ['/drm/'],
                            'exc' : [],
                                'file' : ['drm'], 
                                'func' : [] 
                              }
class_dict['Framework/Network'] = { 'path' : ['/net/'],
                            'exc' : [],
                                    'file' : ['net.h', 'if.', 'if_', 'igmp', 'in.h', 'in6.h', 'ip.h', 'mii', 'notifier',\
                                            'ethtool', 'filter', 'gen_stats', 'rtnetlink', 'socket', 'tcp', 'udp', \
                                            'netlink', 'ipv4', 'ipv6', 'netdev_features', 'icmp', 'neighbour', 'u64_stats_sync'], 
                                    'func' : [] 
                                  }
class_dict['Framework/Generic'] = { 'path' : [],
                            'exc' : [],
                                           'file' : ['device'],    
                                           'func' : []                      
                                         }
class_dict['Framework/Ethernet'] = { 'path' : ['/ethernet/'],
                            'exc' : [],
                                     'file' : ['ethernet'],    
                                     'func' : []                      
                                   }
class_dict['Framework/kobject'] = { 'path' : [],
                                    'file' : ['kobject'],    
                            'exc' : [],
                                    'func' : []                      
                                  }
class_dict['Framework/Input'] = { 'path' : [],
                            'exc' : [],
                                  'file' : [],    
                                  'func' : []                      
                                }
class_dict['Framework/Backlight'] = { 'path' : ['/backlight/'],
                                      'file' : ['backlight'],    
                            'exc' : [],
                                      'func' : []                      
                                    }
class_dict['Framework/hwmon'] = { 'path' : ['/hwmon/'],
                                  'file' : ['hwmon'],    
                            'exc' : [],
                                  'func' : []                      
                                }
class_dict['Framework/MTD'] = { 'path' : ['/mtd/'],
                                'file' : [],    
                            'exc' : [],
                                'func' : []                      
                              }
class_dict['Framework/MFD'] = { 'path' : ['/mfd/'],
                                'file' : ['mfd.c'],    
                            'exc' : [],
                                'func' : []                      
                              }
class_dict['Framework/tty'] = { 'path' : [],
                                'file' : ['tty.h'],    
                            'exc' : [],
                                'func' : []                      
                              }
class_dict['Framework/Block'] = { 'path' : ['/block/'],
                                  'file' : ['block'],    
                            'exc' : [],
                                  'func' : []                      
                                }
class_dict['Framework/Sound'] = { 'path' : ['/sound/'],
                                  'file' : ['sound'],    
                            'exc' : [],
                                  'func' : []                      
                                }
class_dict['Framework/Char'] = { 'path' : ['/char/'],
                                             'file' : [],    
                            'exc' : [],
                                             'func' : []                      
                                           }
# to recognise rwsem-spinlcok.h to Sync/sema
class_dict['Sync/sema'] = { 'path' : [],
                            'file' : ['semaphore', 'rwsem', 'sem.'],
                            'exc' : [],
                            'func' : ['semaphore', 'sema']
                        }
class_dict['Sync/lock'] = { 'path' : [],
                        'file' : ['spinlock', 'rwlock', 'seqlock', 'mutex', 'lockdep'],    
                            'exc' : ['printk'],
                        'func' : ['mutex']                      
                      }
class_dict['IOMMU'] = { 'path' : [],
                      'file' : ['iommu', 'swiotlb'],
                            'exc' : [],
                      'func' : []
                    }
class_dict['Memory'] = { 'path' : ['/mm/'],
                                    'file' : ['mm.', 'mmzone.', 'mmsegment.', 'mmu.', 'pgtable', 'page', 'uaccess', 'gfp', 'mem.', 'hugetlb',\
                                             'memory', 'memcontrol', 'migrate', 'filemap'],    
                            'exc' : [],
                                    'func' : ['alloc', 'free', 'mm_struct']                      
                                  }
class_dict['Memory/net'] = {    'path' : [],
                                'file' : ['sk_buff', 'skbuff'],
                            'exc' : [],
                                'func' : ['skb']
        }
class_dict['Memory/vmalloc'] = {    'path' : [],
                                    'file' : ['vmalloc'],
                            'exc' : [],
                                    'func' : ['vmalloc']
        }
class_dict['Memory/kmalloc'] = {    'path' : [],
                                    'file' : ['slab', 'slob', 'slub'],
                            'exc' : [],
                                    'func' : []
        }
class_dict['Bus/PCI'] = { 'path' : ['/pci/'],
                          'file' : ['pci.'],    
                            'exc' : ['module'],
                          'func' : []                      
                        }
class_dict['Bus/ATA'] = { 'path' : ['/ata/'],
                          'file' : ['pata', 'sata'],    
                            'exc' : [],
                          'func' : []                      
                        }
class_dict['Bus/Platform'] = { 'path' : ['/platform/'],
                               'file' : ['platform.'],    
                            'exc' : [],
                               'func' : []                      
                             }
class_dict['Bus/I2C'] = { 'path' : ['/i2c/'],
                          'file' : ['i2c'],    
                            'exc' : [],
                          'func' : []                      
                        }
class_dict['Bus/SCSI'] = { 'path' : ['/scsi/'],
                           'file' : ['scsi'],    
                            'exc' : [],
                           'func' : []                      
                         }
class_dict['Bus/USB'] = { 'path' : ['/usb/'],
                          'file' : ['usb'],    
                            'exc' : [],
                          'func' : []                      
                        }
class_dict['Bus/SPI'] = { 'path' : [],
                          'file' : [],    
                            'exc' : [],
                          'func' : ['spi_', 'spidev']                      
                        }
class_dict['Bus/Parallel-Port'] = { 'path' : ['/parport/'],
                                    'file' : ['parport'],    
                            'exc' : [],
                                    'func' : []                      
                                  }

class_dict['Bus/Parallel-Port-IDE'] = { 'path' : ['/paride/'],
                                        'file' : ['paride'],    
                            'exc' : [],
                                        'func' : []                      
                                      }
class_dict['Bus/PCMCIA'] = { 'path' : ['/pcmcia/'],
                             'file' : ['pcmcia'],    
                            'exc' : [],
                             'func' : []                      
                          }
class_dict['Klib'] = { 'path' : ['/kernel/'],
                                 'file' : ['bitops', 'kernel', 'list', 'string', 'bitmap', 'cpumask', 'smp', 'types', 'init.', \
                                         'kref', 'personality', 'quota', 'radix-tree', 'tree', 'checksum', 'capability', 'reboot',\
                                         'sysctl', 'stat.', 'nodemask', 'printk', 'log2.', 'percpu', 'jump_label', 'dynamic_queue_limits',\
                                         'list_bl', 'textsearch', 'proportion', 'export', 'tracepoint', 'uprobes'],    
                            'exc' : [],
                                 'func' : ['print']                      
                               }
class_dict['Klib/fs'] = {   'path' : [],
                            'file' : ['elf.', 'binfmts', 'uid', 'gid'],
                            'exc' : [],
                            'func' : ['ELF', 'inode']
        }
class_dict['Security'] = {  'path' : [],
                            'file' : ['security', 'seccomp', 'key', 'cred', 'selinux'],
                            'exc' : [],
                            'func' : []
        }
class_dict['Deferred-Work'] = { 'path' : [],
                                'file' : [],    
                            'exc' : [],
                                'func' : []                      
                              }
class_dict['Cross-Module-Call'] = { 'path' : [],
                                    'file' : [],    
                            'exc' : [],
                                    'func' : []                      
                                  }
class_dict['DMA'] = { 'path' : ['/dma/'],
                                 'file' : ['dma'],    
                            'exc' : [],
                                 'func' : []                      
                               }
class_dict['Resource-Manage'] = { 'path' : [],
                                      'file' : ['resource', 'res_counter'],    
                            'exc' : [],
                                      'func' : ['resource']                      
                                    }
class_dict['Sync/atomic'] = { 'path' : [],
                                  'file' : ['atomic'],    
                            'exc' : [],
                                  'func' : ['atomic']                  
                                }
class_dict['Sync/completion'] = { 'path' : [],
                                  'file' : ['completion'],    
                            'exc' : [],
                                  'func' : ['completion']                  
                                }
class_dict['Sync/rcu'] = { 'path' : [],
                                  'file' : [ 'rcupdate'],    
                            'exc' : [],
                                  'func' : ['rcu_', '_rcu']                  
                                }
class_dict['Sched'] = { 'path' : ['/sched/'],
                                         'file' : ['process.', 'sched', 'thread', 'pid.', 'profile.', 'current', 'pda', 'ptrace',\
                                                  'cgroup', 'nsproxy', 'latencytop', 'taskstats'],    
                            'exc' : [],
                                         'func' : ['ptrace']                      
                                       }
class_dict['Time'] = { 'path' : [],
                                 'file' : ['jiffies', 'time.', 'time_', 'compat'],    
                            'exc' : [],
                                 'func' : []                      
                               }
class_dict['Interrupt'] = {     'path' : [],
                                'file' : ['irq.', 'interrupt', 'irq_', 'irqdesc', 'irqreturn', 'irqflags', 'irqnr', 'pic.', 'apic.',\
                                         'bottom_half'],    
                                'exc' : ['tasklet'],
                                'func' : []                      
                                     }
class_dict['Framebuffer'] = { 'path' : ['/intelfb/'],
                              'file' : [],    
                            'exc' : [],
                              'func' : []                      
                            }
class_dict['Platform'] = { 'path' : ['/byteorder/'],
                                       'file' : ['byteorder', 'processor', 'fixmap.', 'local.h', 'pm.h', 'mpspec.h', 'system.h', 'topology'],    
                            'exc' : [],
                                       'func' : []                      
                                     }
class_dict['Delay'] = { 'path' : [],
                        'file' : ['delay.'],    
                            'exc' : [],
                        'func' : []                      
                      }
class_dict['Delay/timer'] = { 'path' : [],
                        'file' : ['timer'],    
                            'exc' : [],
                        'func' : []                      
                      }
class_dict['Delay/workqueue'] = { 'path' : [],
                        'file' : ['workqueue'],    
                            'exc' : [],
                        'func' : []                      
                      }
class_dict['Delay/waitqueue'] = { 'path' : [],
                        'file' : ['wait.'],    
                            'exc' : [],
                        'func' : []                      
                      }
class_dict['Delay/tasklet'] = { 'path' : [],
                                'file' : [],    
                            'exc' : [],
                                'func' : ['tasklet']                      
                      }
class_dict['Fs/vfs'] = {    'path' : ['/fs/'],
                            'file' : ['vfs', 'fs.h', 'dcache', 'kdev_t', 'nfs', 'poll', 'dqblk', 'fs_struct', 'seq_file',\
                                    'path.', 'shrinker', 'fiemap', 'xattr'],    
                            'exc' : [],
                            'func' : ['vfs']                      
                                    }
class_dict['ACPI'] = { 'path' : ['/acpi/'],
                       'file' : ['acpi'],    
                            'exc' : [],
                       'func' : []                      
                     }

class_dict['Xen-specific'] = { 'path' : [],
                               'file' : [],    
                            'exc' : [],
                               'func' : []                      
                             }
class_dict['Firmware'] = { 'path' : ['/firmware/'],
                           'file' : ['firmware'],    
                            'exc' : [],
                           'func' : []                      
                         }
class_dict['GPIO-Pin-Controller'] = {   'path' : ['/pinctrl/'],
                                        'file' : ['gpio', 'pinctrl'],    
                                        'exc' : [],
                                        'func' : []                      
                                        }
class_dict['Debugger'] = { 'path' : [],
                           'file' : ['bug', 'err.'],    
                            'exc' : [],
                           'func' : []                      
                         }
class_dict['Randomness'] = {    'path' : [],
                                'file' : ['random'],    
                                'exc' : [],
                                'func' : ['random']                      
                           }
class_dict['HDMI'] = {  'path' : [],
                        'file' : ['hdmi'],    
                        'exc' : [],
                        'func' : []                      
                     }
class_dict['Signal'] = {    'path' : [],
                            'file' : ['signal', 'sig.', 'siginfo'],    
                            'exc' : [],
                            'func' : []                      
                       }
class_dict['QoS-Manage'] = {    'path' : [],
                                'file' : ['qos'],    
                                'exc' : [],
                                'func' : []                      
                               }
class_dict['CDROM'] = {     'path' : ['/cdrom/'],
                            'file' : ['cdrom'],    
                            'exc' : [],
                            'func' : []                      
                      }
class_dict['Power/CPU-Freq'] = {    'path' : ['/cpufreq/'],
                                    'file' : ['cpufreq'],    
                                    'exc' : [],
                                    'func' : []                      
                              }
class_dict['Power/Voltage-Current-Regulator'] = {   'path' : [],
                                                    'file' : [],    
                                                    'exc' : [],
                                                    'func' : ['regulator']   
                                          }
class_dict['Power/Manage'] = {   'path' : [],
                                 'file' : ['pm_wakeup'],    
                                 'exc' : [],
                                 'func' : []   
                            }
class_dict['EFI'] = { 'path' : [],
                      'file' : ['efi.', 'efi_', 'efivar', 'efirtc'],    
                      'exc' : [],
                      'func' : []                      
                    }
class_dict['Async-Calls'] = {   'path' : [],
                                'file' : [],    
                                'exc' : [],
                                'func' : []                      
                                   }
class_dict['Multi-core Support'] = {    'path' : [],
                                        'file' : [],    
                                        'exc' : [],
                                        'func' : []                      
                                   }
class_dict['IO-Primitives'] = { 'path' : [],
                                'file' : ['aio.h', 'aio_abi', 'io.h', 'io.c', 'ioctl', 'ioport', 'io-', 'io_', 'iomap'],    
                                'exc' : [],
                                'func' : []                      
                               }
class_dict['drv/net/e1000'] = { 'path' : ['/e1000/'],
                                'file' : ['e1000'],    
                                'exc' : [],
                                'func' : []                      
                                   }
class_dict['Project'] = {       'path' : [],
                                'file' : ['proj'],    
                                'exc' : [],
                                'func' : []                      
                                   }

